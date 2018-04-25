from coursedashboards.views.api.offering.historical import HistoricalCourseData
from django.conf.urls import url
from coursedashboards.views.api.offering.course import CourseData
from coursedashboards.views.api.integration.offering_cgpa import OfferingCGPA
from coursedashboards.views.api.integration.offering_fail_rate import \
    OfferingFailRate
from coursedashboards.views.api.integration.offering_majors import \
    OfferingMajors
from coursedashboards.views.index import index
from coursedashboards.views.page import user_login, logout

course_regex = r'^api/v1/course/(?i)(?P<year>\d{4})-'\
               r'(?P<quarter>[A-Za-z]+)-'\
               r'(?P<curriculum>[&% 0-9a-z]+)-'\
               r'(?P<course_number>\d{3})-'\
               r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)'

urlpatterns = [
    # Home
    url(r'^$', index, name='home'),
    url(course_regex + r'/past$',
        HistoricalCourseData.as_view(),
        name='historic_course_data'),
    url(course_regex + r'$',
        CourseData.as_view(),
        name='course_data_for_term'),
    url(course_regex + r'/majors/(?P<num_majors>\d)$',
        OfferingMajors.as_view(),
        name='course_majors'),
    url(course_regex + r'/fail_rate$',
        OfferingFailRate.as_view(),
        name='course_fail_rate'),
    url(course_regex + r'/cgpa$',
        OfferingCGPA.as_view(),
        name='course_cgpa'),
    url(r'^login', user_login),
    url(r'^logout', logout, name="coda_logout")
]
