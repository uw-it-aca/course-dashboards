# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from coursedashboards.views.api.offering.historical import HistoricalCourseData
from django.urls import re_path
from coursedashboards.views.api.offering.course import CourseData
from coursedashboards.views.api.integration.offering_cgpa import OfferingCGPA
from coursedashboards.views.api.integration.offering_fail_rate import \
    OfferingFailRate
from coursedashboards.views.api.integration.offering_majors import \
    OfferingMajors
from coursedashboards.views.index import index
from coursedashboards.views.page import user_login, logout

course_regex = r'^api/v1/course/(?P<year>\d{4})-'\
               r'(?P<quarter>[A-Za-z]+)-'\
               r'(?P<curriculum>[&% 0-9A-Za-z]+)-'\
               r'(?P<course_number>\d{3})-'\
               r'(?P<section_id>[A-Za-z][0-9A-Za-z]?)'

urlpatterns = [
    # Home
    re_path(r'^$', index, name='home'),
    re_path(course_regex + r'/past$',
            HistoricalCourseData.as_view(),
            name='historic_course_data'),
    re_path(course_regex + r'$',
            CourseData.as_view(),
            name='course_data_for_term'),
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
