# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import utc
from datetime import datetime, timedelta
import logging
from coursedashboards.models import (
    Term, Instructor, Course, CourseOffering,
    Registration, Major, StudentMajor)
from coursedashboards.dao.exceptions import (
    MalformedOrInconsistentUser, NoTermAfterCurrent)
from coursedashboards.dao.term import (
    get_given_and_previous_quarters, get_term_after_current)
from coursedashboards.dao.pws import get_person_by_netid
from coursedashboards.dao.gws import get_effective_members
from coursedashboards.dao.user import user_from_person
from coursedashboards.dao.section import (
    get_changed_sections, get_section_from_url)
from coursedashboards.dao.person import get_person_from_regid
from coursedashboards.dao.enrollment import (
    get_student_majors_for_regid_and_term)
from coursedashboards.dao.registration import (
    get_active_registrations_for_section)
from coursedashboards.dao.canvas import canvas_course_url_from_section
from restclients_core.exceptions import DataFailureException


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
            '--next', action='store_true',
            help='Include next term if appropriate')
        parser.add_argument(
            '--instructor', dest='instructor', default='',
            help='netid or uw group containing instructors to load')
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ignore change since date, loading all relevant courses',
        )

    def handle(self, *args, **options):
        logger.debug(
            'load_data_for_term: term={} instructor={} previous={}'.format(
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

        if options.get('next'):
            try:
                sws_terms.append(get_term_after_current(sws_terms[-1]))
            except NoTermAfterCurrent:
                pass

        for sws_term in sws_terms:
            logger.info('loading term: {},{}'.format(
                sws_term.quarter, sws_term.year))

            term, created = Term.objects.get_or_create(
                quarter=sws_term.quarter, year=sws_term.year)
            changed_since = term.last_queried
            if options['force'] or not changed_since:
                delta = timedelta(days=365)
                changed_since = sws_term.first_day_quarter - delta

            changed_date = datetime.utcnow().replace(tzinfo=utc)
            for instructor in instructors:
                logger.debug('loading instructor: {}'.format(instructor))
                params = {
                    'transcriptable_course': 'yes',
                    'include_secondaries': False,
                    'page_size': 500
                }

                if instructor:
                    person = get_person_by_netid(instructor)
                    params['reg_id'] = person.uwregid
                    params['search_by'] = 'Instructor'

                section_refs = get_changed_sections(
                    changed_since, term, **params)

                for section_ref in section_refs:
                    try:
                        section = get_section_from_url(section_ref.url)
                        self._load_section(section, term, sws_term)
                    except DataFailureException as ex:
                        logger.error("section fetch: {}: {}".format(
                            section_ref.url, ex))
                        continue
                    for joint_section_url in section.joint_section_urls:
                        try:
                            joint_section = get_section_from_url(
                                joint_section_url)
                            self._load_section(joint_section, term, sws_term)
                        except DataFailureException as ex:
                            logger.error("section fetch: {}: {}".format(
                                section_ref.url, ex))
                            continue

            # remember the last time we crawled this term
            term.last_queried = changed_date
            term.save()

    @transaction.atomic
    def _load_section(self, section, term, sws_term):
        if not section.is_primary_section:
            logger.info('skip non-primary: {}'.format(
                section.section_label()))
            return

        course, created = Course.objects.get_or_create(
            curriculum=section.curriculum_abbr,
            course_number=section.course_number,
            section_id=section.section_id)

        # update course title
        if (section.course_title_long and
                course.course_title != section.course_title_long):
            course.course_title = section.course_title_long[:64]
            course.save()

        if section.is_withdrawn():
            try:
                self._remove_course(term, course)
            except Course.DoesNotExist:
                pass

            return

        logger.info('load: {}'.format(self._offering_string(term, course)))
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
                limit_estimate_enrollment=section.limit_estimate_enrollment,
                canvas_course_url=canvas_course_url_from_section(section))

    def _instructors_from_section(self, term, course, section):
        prior_instructors = list(Instructor.objects.filter(
            term=term, course=course).values_list('user_id', flat=True))
        section_instructors = section.get_instructors()
        for section_instructor in section_instructors:
            if not (section_instructor and
                    section_instructor.uwnetid and
                    section_instructor.uwregid):
                logger.info(
                    'incomplete instructor: netid: {}, regid: {}'.format(
                        getattr(section_instructor, 'uwnetid', "null"),
                        getattr(section_instructor, 'uwregid', "null")))
                continue
            try:
                user = user_from_person(section_instructor)
            except MalformedOrInconsistentUser:
                continue
            except Exception as ex:
                logger.info(f"cannot load instructor: {ex}")
                continue

            inst_obj, created = Instructor.objects.get_or_create(
                user=user, course=course, term=term)

            if inst_obj.user_id in prior_instructors:
                prior_instructors.remove(inst_obj.user_id)

            logger.debug('{} instructor: netid:{}, course: {}'.format(
                'new' if created else 'update',
                user.uwnetid, self._offering_string(term, course)))

        # remove prior instructors
        if len(prior_instructors):
            logger.debug('drop instructor: {} for course: {}'.format(
                prior_instructors, self._offering_string(term, course)))
            Instructor.objects.filter(
                user_id__in=prior_instructors,
                term=term, course=course).delete()

    def _registrations_from_section(self, term, course, section):
        prior_registrations = list(Registration.objects.filter(
            term=term, course=course).values_list('user_id', flat=True))
        for registration in get_active_registrations_for_section(section):
            if not (registration.person and
                    registration.person.uwnetid and
                    registration.person.uwregid):
                logger.info(
                    'incomplete registration: netid: {}, regid: {}'.format(
                        getattr(registration.person, 'uwnetid', "null"),
                        getattr(registration.person, 'uwregid', "null")))
                continue
            try:
                user = user_from_person(registration.person)
            except MalformedOrInconsistentUser:
                continue

            reg_obj, created = Registration.objects.get_or_create(
                user=user, course=course, term=term)

            # update grade/credits
            if (reg_obj.grade != registration.grade or
                    reg_obj.credits != registration.credits or
                    reg_obj.is_repeat != registration.repeat_course):
                reg_obj.grade = registration.grade
                reg_obj.is_repeat = registration.repeat_course
                reg_obj.credits = registration.credits
                reg_obj.save()

            try:
                if created:
                    sws_person = get_person_from_regid(user.uwregid)
                    if sws_person.last_enrolled:
                        last_term, created = Term.objects.get_or_create(
                            year=sws_person.last_enrolled.year,
                            quarter=sws_person.last_enrolled.quarter)
                        if user.last_enrolled != last_term:
                            user.last_enrolled = last_term
                            user.save()
            except DataFailureException:
                pass

            if reg_obj.user_id in prior_registrations:
                prior_registrations.remove(reg_obj.user_id)

            logger.debug('{} registration: netid:{}, course: {}'.format(
                'new' if created else 'update',
                user.uwnetid, self._offering_string(term, course)))

        # remove dropped registrations
        if len(prior_registrations):
            logger.debug('drop registrations: {} for course: {}'.format(
                prior_registrations, self._offering_string(term, course)))
            Registration.objects.filter(
                user_id__in=prior_registrations,
                term=term, course=course).delete()

    def _collect_majors(self, registrations, course, term, sws_term):
        majors = {}
        for reg in registrations:
            for student_major in get_student_majors_for_regid_and_term(
                    reg.user.uwregid, sws_term):
                if student_major.major_name:
                    major, created = Major.objects.get_or_create(
                        major=student_major.major_name,
                        degree_level=student_major.degree_level)
                    StudentMajor.objects.get_or_create(
                        user=reg.user, major=major, term=term)

                if student_major.major_name in majors:
                    majors[student_major.major_name] += 1
                else:
                    majors[student_major.major_name] = 1

    def _remove_course(self, term, course):
        logger.info('remove: {}'.format(self._offering_string(term, course)))
        Registration.objects.filter(term=term, course=course).delete()
        Instructor.objects.filter(term=term, course=course).delete()
        CourseOffering.objects.filter(term=term, course=course).delete()

    def _offering_string(self, term, course):
        return '{},{}'.format(term, course)
