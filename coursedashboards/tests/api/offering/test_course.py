# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.tests.api import CodaApiTest
import json


class TestCourseAPIs(CodaApiTest):

    def get_course_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'course_data_for_term', *args, **kwargs)

    def get_profile_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'course_student_data_for_term', *args, **kwargs)

    def test_course_api(self):
        self.set_user('bill')
        response = self.get_course_response(kwargs={
            'year': '2014', 'quarter': 'winter', 'curriculum': "POL S",
            'course_number': "201", 'section_id': "A"})

        self.assertEquals(response.status_code, 200)

        course = json.loads(response.content)

        self.assertEquals(course['current_enrollment'], 190)
        self.assertEquals(course['current_repeating'], 5)
        self.assertEquals(course['median_course_grade'], 3.4)

    def test_profile(self):
        self.set_user('bill')
        response = self.get_profile_response(kwargs={
            'year': '2014', 'quarter': 'winter', 'curriculum': "POL S",
            'course_number': "201", 'section_id': "A"})

        self.assertEquals(response.status_code, 200)

        profile = json.loads(response.content)

        self.assertEquals(len(profile.keys()), 4)

        self.assertEquals(profile['eop']['n'], 22)
        self.assertEquals(profile['transfer']['n'], 15)
        self.assertEquals(profile['disability']['n'], 12)
        self.assertEquals(profile['probation']['n'], 4)
