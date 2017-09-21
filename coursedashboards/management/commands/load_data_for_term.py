from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from datetime import datetime, timedelta
import logging
from coursedashboards.models import (
    Term, Instructor, Course, CourseOffering,
    Registration, Major, StudentMajor)
from coursedashboards.dao.exceptions import (
    MalformedOrInconsistentUser)
from coursedashboards.dao.term import get_given_and_previous_quarters
from coursedashboards.dao.pws import get_person_by_netid
from coursedashboards.dao.gws import get_effective_members
from coursedashboards.dao.user import user_from_person
from uw_sws.section import get_changed_sections_by_term, get_section_by_url
from uw_sws.person import get_person_by_regid
from uw_sws.registration import get_active_registrations_by_section
from uw_sws.enrollment import get_enrollment_by_regid_and_term
from uw_canvas.courses import Courses as CanvasCourses


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populate user, major, course, instructor tables for specified term"

    def add_arguments(self, parser):
        parser.add_argument(
            '--term', dest='term', default=None,
            help='term to load yyyy,quarter')
        parser.add_argument(
            '--previous', dest='previous_terms', default=0, type=int,
            help='count of previous terms to include')
        parser.add_argument(
            '--instructor', dest='instructor', default='',
            help='netid or uw group containing instructors to load')

    def handle(self, *args, **options):
        logger.debug(
            'load_data_for_term: term=%s instructor=%s previous=%s' % (
                options.get('term', ''), options.get('instructor', ''),
                options.get('previous_terms')))
        term_string = options.get('term')

        instructor = options.get('instructor')
        if '_' in instructor:
            instructors = [x.name for x in get_effective_members(
                instructor) if x.is_uwnetid()]
        else:
            instructors = [instructor]

        sws_terms = get_given_and_previous_quarters(
            term_string, options.get('previous_terms'))
        for sws_term in sws_terms:
            logger.info('loading term: %s,%s' % (
                sws_term.quarter, sws_term.year))

            term, created = Term.objects.get_or_create(
                quarter=sws_term.quarter, year=sws_term.year)
            changed_since = term.last_queried
            if not changed_since:
                delta = timedelta(days=365)
                changed_since = sws_term.first_day_quarter - delta

            changed_date = datetime.utcnow().replace(tzinfo=utc)
            for instructor in instructors:
                logger.debug('loading instructor: %s' % (instructor))
                params = {
                    'transcriptable_course': 'yes',
                    'include_secondaries': False,
                    'page_size': 500
                }

                if instructor:
                    person = get_person_by_netid(instructor)
                    params['reg_id'] = person.uwregid
                    params['search_by'] = 'Instructor'

                section_refs = get_changed_sections_by_term(
                    changed_since, term, **params)

                for section_ref in section_refs:
                    section = get_section_by_url(section_ref.url)
                    self._load_section(section, term, sws_term)
                    for joint_section_url in section.joint_section_urls:
                        joint_section = get_section_by_url(joint_section_url)
                        self._load_section(joint_section, term, sws_term)

            # remember the last time we crawled this term
            term.last_queried = changed_date
            term.save()

    def _load_section(self, section, term, sws_term):
        course, created = Course.objects.get_or_create(
            curriculum=section.curriculum_abbr,
            course_number=section.course_number,
            section_id=section.section_id)

        if section.is_withdrawn:
            try:
                self._remove_course(term, course)
            except Course.DoesNotExist:
                pass

            return

        logger.info('load: %s' % (
            self._offering_string(term, course)))
        self._course_offering_from_section(term, course, section)
        self._instructors_from_section(term, course, section)
        self._registrations_from_section(term, course, section)

        registrations = Registration.objects.filter(term=term, course=course)
        self._collect_majors(registrations, course, term, sws_term)

    def _course_offering_from_section(self, term, course, section):
        try:
            co = CourseOffering.objects.get(term=term, course=course)
            co.current_enrollment = section.current_enrollment
            co.limit_estimate_enrollment = section.limit_estimate_enrollment
            co.save()
        except CourseOffering.DoesNotExist:
            co = CourseOffering.objects.create(
                term=term, course=course,
                current_enrollment=section.current_enrollment,
                limit_estimate_enrollment=section.limit_estimate_enrollment)

        try:
            canvas_course = CanvasCourses().get_course_by_sis_id(
                section.canvas_course_sis_id())
            co.canvas_course_url = canvas_course.course_url
            co.save()
        except Exception as ex:
            logger.info("cannot add canvas url: %s" % (ex))

    def _instructors_from_section(self, term, course, section):
        prior_instructors = list(Instructor.objects.filter(
            term=term, course=course).values_list('user_id', flat=True))
        section_instructors = section.get_instructors()
        for section_instructor in section_instructors:
            if not (section_instructor and
                    section_instructor.uwnetid and
                    section_instructor.uwregid):
                logger.info('incomplete instructor: netid: %s, regid: %s' % (
                    getattr(section_instructor, 'uwnetid', "null"),
                    getattr(section_instructor, 'uwregid', "null")))
                continue
            try:
                user = user_from_person(section_instructor)
            except MalformedOrInconsistentUser:
                continue

            inst_obj, created = Instructor.objects.get_or_create(
                user=user, course=course, term=term)

            if not created and id in prior_instructors:
                prior_instructors.remove(id)

            logger.debug('%s instructor: netid:%s, course: %s' % (
                'new' if created else 'update',
                user.uwnetid, self._offering_string(term, course)))

        # remove prior instructors
        if len(prior_instructors):
            Instructor.objects.filter(
                user_id__in=prior_instructors,
                term=term, course=course).delete()

    def _registrations_from_section(self, term, course, section):
        prior_registrations = list(Registration.objects.filter(
            term=term, course=course).values_list('user_id', flat=True))
        registrations = get_active_registrations_by_section(section)
        for registration in registrations:
            if not (registration.person and
                    registration.person.uwnetid and
                    registration.person.uwregid):
                logger.info('incomplete registration: netid: %s, regid: %s' % (
                    getattr(registration.person, 'uwnetid', "null"),
                    getattr(registration.person, 'uwregid', "null")))
                continue
            try:
                user = user_from_person(registration.person)
            except MalformedOrInconsistentUser:
                continue

            reg_obj, created = Registration.objects.get_or_create(
                user=user, course=course, term=term)

            reg_obj.grade = registration.grade
            reg_obj.is_repeat = registration.repeat_course
            reg_obj.save()

            sws_person = get_person_by_regid(user.uwregid)
            if sws_person.last_enrolled:
                last_term, created = Term.objects.get_or_create(
                    year=sws_person.last_enrolled.year,
                    quarter=sws_person.last_enrolled.quarter)
                user.last_enrolled = last_term
                user.save()

            if not created and id in prior_registrations:
                prior_registrations.remove(id)

            logger.debug('%s registration: netid:%s, course: %s' % (
                'new' if created else 'update',
                user.uwnetid, self._offering_string(term, course)))

        # remove dropped registrations
        if len(prior_registrations):
            Registration.objects.filter(
                user_id__in=prior_registrations).delete()

    def _collect_majors(self, registrations, course, term, sws_term):
        majors = {}
        for reg in registrations:
            student_majors = self._get_student_major(reg.user, sws_term)
            for student_major in student_majors:
                if student_major.major_name:
                    major, created = Major.objects.get_or_create(
                        major=student_major.major_name)
                    StudentMajor.objects.get_or_create(
                        user=reg.user, major=major, term=term)

                if major in majors:
                    majors[major] += 1
                else:
                    majors[major] = 1

    def _get_student_major(self, user, sws_term):
        enrollment = get_enrollment_by_regid_and_term(user.uwregid, sws_term)
        return enrollment.majors

    def _remove_course(self, term, course):
        logger.info('remove: %s' % (
            self._offering_string(term, course)))
        Registration.objects.filter(term=term, course=course).delete()
        Instructor.objects.filter(term=term, course=course).delete()
        CourseOffering.objects.filter(term=term, course=course).delete()

    def _offering_string(self, term, course):
        return '%s,%s' % (term, course)
