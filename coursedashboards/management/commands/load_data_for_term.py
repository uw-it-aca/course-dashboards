from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import utc
from datetime import datetime
import logging
from coursedashboards.models import (
    Term, User, Instructor, Course, CourseOffering,
    Registration, Major, StudentMajor)
from coursedashboards.dao.exceptions import (
    MalformedOrInconsistentUser)
from uw_gws import GWS
from uw_pws import PWS
from uw_pws.models import Person
from uw_sws.term import (
    get_current_term, get_term_by_year_and_quarter, get_term_before)
from uw_sws.section import get_changed_sections_by_term, get_section_by_url
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
            '--previous', dest='previous', default=0, type=int,
            help='count of previous terms to include')
        parser.add_argument(
            '--instructor', dest='instructor', default=None,
            help='netid or uw group containing instructors to load')

    def handle(self, *args, **options):
        logger.debug(
            'load_data_for_term: term=%s instructor=%s previous=%s' % (
                options.get('term', ''), options.get('instructor', ''),
                options.get('previous_terms', 0)))
        term_string = options.get('term')
        if term_string:
            year, quarter = term_string.split(',', 1)
            sws_term = get_term_by_year_and_quarter(quarter, year)
        else:
            sws_term = get_current_term()

        instructor = options.get('instructor', '')
        if '_' in instructor:
            instructors = GWS().get_effective_members(instructor)
        else:
            instructors = [instructor]

        for i in range(options.get('previous_terms', 0), -1, -1):
            logger.info('loading term: %s,%s' % (
                sws_term.quarter, sws_term.year))

            term, created = Term.objects.get_or_create(
                quarter=sws_term.quarter, year=sws_term.year)
            changed_since = term.last_queried if term.last_queried else ''

            changed_date = datetime.utcnow().replace(tzinfo=utc)
            for instructor in instructors:
                logger.debug('loading instructor: %s' % (instructor))

                person = PWS().get_person_by_netid(instructor) if (
                    instructor) else Person(uwregid='')
                section_refs = get_changed_sections_by_term(
                    changed_since, term,
                    transcriptable_course='yes',
                    search_by='Instructor',
                    reg_id=person.uwregid,
                    include_secondaries=False,
                    page_size=500)

                for section_ref in section_refs:
                    section = get_section_by_url(section_ref.url)
                    self._load_section(section, term, sws_term)
                    for joint_section_url in section.joint_section_urls:
                        joint_section = get_section_by_url(joint_section_url)
                        self._load_section(joint_section, term, sws_term)

            # remember the last time we crawled this term
            term.last_queried = changed_date
            term.save()

            if i > 0:
                sws_term = get_term_before(sws_term)

    def _load_section(self, section, term, sws_term):
        course, created = Course.objects.get_or_create(
            curriculum=section.curriculum_abbr,
            course_number=section.course_number,
            section_id=section.section_id)

        if section.is_withdrawn:
            try:
                course = Course.objects.get(course=course, term=term)
                self.remove_course(term, course)
                logger.info('withdrawn: %s' % (
                    self._offering_string(term, course)))
            except Course.DoesNotExist:
                pass

            return

        logger.info('loading: %s' % (self._offering_string(term, course)))
        self._course_offering_from_section(term, course, section)
        self._instructors_from_section(term, course, section)
        self._registrations_from_section(term, course, section)

        registrations = Registration.objects.filter(term=term, course=course)
        self._collect_student_majors(registrations, sws_term)

    def _user_from_person(self, person):
        try:
            user, created = User.objects.get_or_create(
                uwnetid=person.uwnetid,
                uwregid=person.uwregid,
                display_name=person.display_name,
                email=person.email1
            )
        except IntegrityError as ex:
            logger.error('user unique violation: %s (%s): %s' % (
                person.uwnetid, person.uwregid, ex))
            raise MalformedOrInconsistentUser()

        return user

    def _course_offering_from_section(self, term, course, section):
        offering, created = CourseOffering.objects.update_or_create(
            term=term, course=course,
            current_enrollment=section.current_enrollment,
            limit_estimate_enrollment=section.limit_estimate_enrollment)

        try:
            canvas_course = CanvasCourses().get_course_by_sis_id(
                section.canvas_course_sis_id())
            offering.canvas_course_url = canvas_course.course_url
            offering.save()
        except Exception as ex:
            logger.error("cannot add canvas url: %s" % (ex))

    def _instructors_from_section(self, term, course, section):
        prior_instructors = Instructor.objects.filter(term=term, course=course)
        section_instructors = section.get_instructors()
        for section_instructor in section_instructors:
            try:
                user = self._user_from_person(section_instructor)
                prior_instructors.get(user=user)
                prior_instructors = prior_instructors.exclude(user=user)
            except MalformedOrInconsistentUser:
                pass
            except Instructor.DoesNotExist:
                Instructor.objects.create(
                    user=user, term=term, course=course)

        # remove prior instructors
        prior_instructors.delete()

    def _registrations_from_section(self, term, course, section):
        prior_registrations = Registration.objects.filter(
            term=term, course=course)
        registrations = get_active_registrations_by_section(section)
        for registration in registrations:
            try:
                user = self._user_from_person(registration.person)
                user_reg = prior_registrations.get(user=user)
                if user_reg.grade != registration.grade:
                    user_reg.grade = registration.grade
                    user_reg.save()

                prior_registrations = prior_registrations.exclude(user=user)
                logger.debug('registration: netid:%s, course: %s' % (
                    registration.person.uwnetid,
                    self._offering_string(term, course)))
            except MalformedOrInconsistentUser:
                pass
            except Registration.DoesNotExist:
                Registration.objects.create(
                    user=user, term=term, course=course,
                    grade=registration.grade,
                    is_repeat=registration.repeat_course)

        # remove dropped registrations
        prior_registrations.delete()

    def _collect_student_majors(self, registrations, sws_term):
        for reg in registrations:
            student_majors = self._get_student_major(reg.user, sws_term)
            for student_major in student_majors:
                major, created = Major.objects.get_or_create(
                    major=student_major.major_name)
                StudentMajor.objects.get_or_create(
                    user=reg.user, major=major)

    def _get_student_major(self, user, sws_term):
        enrollment = get_enrollment_by_regid_and_term(user.uwregid, sws_term)
        return enrollment.majors

    def _remove_course(self, term, course):
        Registration.objects.filter(term=term, course=course).delete()
        Instructor.objects.filter(term=term, course=course).delete()
        CourseOffering.objects.get(term=term, course=course)

    def _offering_string(self, term, course):
        return '%s,%s,%s,%s/%s' % (
                term.year, term.quarter, course.curriculum,
                course.course_number, course.section_id)
