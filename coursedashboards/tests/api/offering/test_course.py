# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.tests.api import CodaApiTest
import json


class TestCourseAPIs(CodaApiTest):

    course = {
        'year': '2014', 'quarter': 'winter', 'curriculum': "POL S",
        'course_number': "201", 'section_id': "A"}

    def get_course_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'course_data_for_term', *args, **kwargs)

    def get_profile_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'course_student_data_for_term', *args, **kwargs)

    def get_historic_course_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_course_data', *args, **kwargs)

    def get_past_performance_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_course_performance', *args, **kwargs)

    def get_past_concurrent_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_concurrent_courses', *args, **kwargs)

    def get_student_major_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_student_majors', *args, **kwargs)

    def get_graduated_major_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_graduated_major', *args, **kwargs)

    def get_historic_gpas_response(self, *args, **kwargs):
        return self.get_response_by_reverse(
            'historic_course_gpas', *args, **kwargs)

    def test_course_api(self):
        self.set_user('bill')
        response = self.get_course_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        course = json.loads(response.content)

        self.assertEquals(course['current_enrollment'], 190)
        self.assertEquals(course['current_repeating'], 5)
        self.assertEquals(course['median_course_grade'], 3.4)

    def test_profile(self):
        self.set_user('bill')
        response = self.get_profile_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        profile = json.loads(response.content)

        self.assertEquals(len(profile.keys()), 4)

        self.assertEquals(profile['eop']['n'], 22)
        self.assertEquals(profile['transfer']['n'], 15)
        self.assertEquals(profile['disability']['n'], 12)
        self.assertEquals(profile['probation']['n'], 4)

    def test_historic_course_api(self):
        self.set_user('bill')
        response = self.get_historic_course_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        past_offerings = payload['past_offerings']
        sections = payload['sections']

        self.assertEquals(len(past_offerings['terms']), 3)
        self.assertEquals(past_offerings['enrollment'], 394)
        self.assertEquals(len(sections), 1)
        self.assertEquals(len(sections['2013']), 3)

    def test_past_performance_api(self):
        self.set_user('bill')
        response = self.get_past_performance_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        performance = payload['performance']

        self.assertEquals(performance['enrollment'], 394)
        self.assertEquals(performance['offering_count'], 3)
        self.assertEquals(len(performance['course_grades']), 370)

    def test_past_concurrent_api(self):
        self.set_user('bill')
        response = self.get_past_concurrent_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        concurrent = payload['concurrent_courses']

        self.assertEquals(len(concurrent), 2)

    def test_past_student_major_api(self):
        self.set_user('bill')
        response = self.get_student_major_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        majors = payload['student_majors']

        self.assertEquals(len(majors), 20)

    def test_past_graduated_major_api(self):
        self.set_user('bill')
        response = self.get_graduated_major_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        majors = payload['graduated_majors']

        self.assertEquals(len(majors), 20)

    def test_past_historic_gpas_api(self):
        self.set_user('bill')
        response = self.get_historic_gpas_response(kwargs=self.course)

        self.assertEquals(response.status_code, 200)

        payload = json.loads(response.content)
        gpas = payload['gpas']
