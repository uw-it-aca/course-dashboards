# Copyright 2025 UW-IT, University of Washington
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

    def test_course_apis(self):
        self.set_user('bill')

        response = self.get_course_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        course = json.loads(response.content)

        self.assertEqual(course['current_enrollment'], 190)
        self.assertEqual(course['current_repeating'], 5)
        self.assertEqual(course['median_course_grade'], 3.4)

        # def test_profile
        response = self.get_profile_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        profile = json.loads(response.content)

        self.assertEqual(len(profile.keys()), 4)

        self.assertEqual(profile['eop']['n'], 22)
        self.assertEqual(profile['transfer']['n'], 15)
        self.assertEqual(profile['disability']['n'], 12)
        self.assertEqual(profile['probation']['n'], 4)

        # test_historic_course_api
        response = self.get_historic_course_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        past_offerings = payload['past_offerings']
        sections = payload['sections']

        self.assertEqual(len(past_offerings['terms']), 3)
        self.assertEqual(past_offerings['enrollment'], 394)
        self.assertEqual(len(sections), 1)
        self.assertEqual(len(sections['2013']), 3)

        # test_past_performance_api
        response = self.get_past_performance_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        performance = payload['performance']

        self.assertEqual(performance['enrollment'], 394)
        self.assertEqual(performance['offering_count'], 3)
        self.assertEqual(len(performance['course_grades']), 370)

        # test_past_concurrent_api
        response = self.get_past_concurrent_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        concurrent = payload['concurrent_courses']

        self.assertEqual(len(concurrent), 2)

        # test_past_student_major_api(self):
        response = self.get_student_major_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        majors = payload['student_majors']

        self.assertEqual(len(majors), 20)

        # test_past_graduated_major_api
        response = self.get_graduated_major_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        majors = payload['graduated_majors']

        self.assertEqual(len(majors), 20)

        # test_past_historic_gpas_api
        response = self.get_historic_gpas_response(kwargs=self.course)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        gpas = payload['gpas']
