# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.offering.historical import (
    HistoricalPerformance, HistoricalCourseData, HistoricalConcurrentCourses,
    HistoricalCourseGPAs, HistoricalStudentMajors,
    HistoricalGraduatedMajors)
from django.urls import re_path
from coursedashboards.views.api.offering.course import CourseData
from coursedashboards.views.api.offering.profile import CourseProfileData
from coursedashboards.views.api.offering.textbooks import CourseTextbookData
from coursedashboards.views.api.integration.offering_cgpa import OfferingCGPA
from coursedashboards.views.api.integration.offering_fail_rate import (
    OfferingFailRate)
from coursedashboards.views.api.integration.offering_majors import (
    OfferingMajors)
from coursedashboards.views.api.introduction import Introduction
from coursedashboards.views.index import index
from coursedashboards.views.page import user_login, logout

course_regex = (
    r'^api/v1/course/(?P<year>\d{4})-'
    r'(?P<quarter>[A-Za-z]+)-'
    r'(?P<curriculum>[&% 0-9A-Za-z]+)-'
    r'(?P<course_number>\d{3})-'
    r'(?P<section_id>[A-Za-z][0-9A-Za-z]?)')

urlpatterns = [
    # Home
    re_path(r'^$', index, name='home'),
    re_path(r'api/v1/user/(?P<netid>[a-z][a-z0-9\-\_\.]{,127})/introduction',
            Introduction.as_view(),
            name='coda_introduction'),
    re_path(course_regex + r'/past/performance/?',
            HistoricalPerformance.as_view(),
            name='historic_course_performance'),
    re_path(course_regex + r'/past/concurrent/?',
            HistoricalConcurrentCourses.as_view(),
            name='historic_concurrent_courses'),
    re_path(course_regex + r'/past/gpas/?',
            HistoricalCourseGPAs.as_view(),
            name='historic_course_gpas'),
    re_path(course_regex + r'/past/studentmajor/?',
            HistoricalStudentMajors.as_view(),
            name='historic_student_majors'),
    re_path(course_regex + r'/past/graduatedmajor/?',
            HistoricalGraduatedMajors.as_view(),
            name='historic_graduated_major'),
    re_path(course_regex + r'/past/?',
            HistoricalCourseData.as_view(),
            name='historic_course_data'),
    re_path(course_regex + r'$',
            CourseData.as_view(),
            name='course_data_for_term'),
    re_path(course_regex + r'/profile$',
            CourseProfileData.as_view(),
            name='course_student_data_for_term'),
    re_path(course_regex + r'/textbooks$',
            CourseTextbookData.as_view(),
            name='course_textbook_data_for_term'),
    re_path(course_regex + r'/majors/(?P<num_majors>\d)$',
            OfferingMajors.as_view(),
            name='course_majors'),
    re_path(course_regex + r'/fail_rate$',
            OfferingFailRate.as_view(),
            name='course_fail_rate'),
    re_path(course_regex + r'/cgpa$',
            OfferingCGPA.as_view(),
            name='course_cgpa'),
    re_path(r'^login', user_login),
    re_path(r'^logout', logout, name="coda_logout")
]
