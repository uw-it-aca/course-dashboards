# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint


class HistoricalCourseData(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_json_object(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=self.get_current_instructor())


class HistoricalPerformance(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_performance_data(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=self.get_current_instructor())


class HistoricalConcurrentCourses(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_concurrent_courses(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=self.get_current_instructor())


class HistoricalCourseGPAs(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_course_gpas(
            courses=self.request.GET.get('courses', ''))


class HistoricalStudentMajors(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_student_majors(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=self.get_current_instructor())


class HistoricalGraduatedMajors(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_graduated_majors(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=self.get_current_instructor())
