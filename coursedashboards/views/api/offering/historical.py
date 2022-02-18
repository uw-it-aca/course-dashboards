# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.dao.user import get_current_user


class HistoricalCourseData(CoDaEndpoint):
    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_json_object(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)


class HistoricalPerformance(CoDaEndpoint):
    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_performance_data(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)


class HistoricalConcurrentCourses(CoDaEndpoint):
    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_concurrent_courses(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)


class HistoricalCourseGPAs(CoDaEndpoint):
    def get_data(self, offering):
        return offering.past_offerings_course_gpas(
            courses=self.request.GET.get('courses', ''))


class HistoricalStudentMajors(CoDaEndpoint):
    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_student_majors(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)


class HistoricalGraduatedMajors(CoDaEndpoint):
    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_graduated_majors(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)
