# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from blti.views import BLTILaunchView
from coursedashboards.models import Term, Instructor, Course, CourseOffering
from coursedashboards.models.user import User
import logging
import re


logger = logging.getLogger(__name__)


class CourseLaunchView(BLTILaunchView):
    template_name = 'course.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        if self.blti.course_sis_id:
            try:
                instructor_netid = self.blti.user_login_id
                course_id = self._sis_id_components(self.blti.course_sis_id)
                sections, historic = self._get_course_data(
                    instructor_netid, course_id)
                return {
                    'instructor': instructor_netid,
                    'sections': sections,
                    'historic': historic
                } | course_id
            except Exception as ex:
                logger.error(
                    f"LTI launch {self.blti.course_sis_id} error: {ex}")

        return {'error': f"Course Dashboard is not available"}

    def _sis_id_components(self, sis_id):
        RE_COURSE_SIS_ID = re.compile(
            r"(^\d{4})-"                           # year
            r"((?:winter|spring|summer|autumn))-"  # quarter
            r"([\w& ]+)-"                          # curriculum
            r"(\d{3})-"                            # course number
            r"([A-Z][A-Z0-9]?)"                    # section id
            r"((?:-[A-F0-9]{32})?)$",              # ind. study inst regid
            re.VERBOSE)

        match = RE_COURSE_SIS_ID.match(sis_id)

        return {
            "year": match.group(1),
            "quarter": match.group(2),
            "curriculum": match.group(3),
            "course_number": match.group(4),
            "section_label": match.group(5)
        } if match else {}

    def _get_course_data(self, instructor_netid, course_id):
        term = Term.objects.get(
            year=course_id['year'], quarter=course_id['quarter'])
        course = Course.objects.get(curriculum=course_id['curriculum'],
                                    course_number=course_id['course_number'],
                                    section_id=course_id['section_label'])
        instructor = Instructor.objects.get(
            user__uwnetid=instructor_netid, course=course, term=term)
        offering = CourseOffering.objects.get(
            course=course, term=term)
        return [offering.brief_json_object()], {str(offering): {}}
