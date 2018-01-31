from coursedashboards.views.api.offering.historical import HistoricalCourseData
from django.conf.urls import url
from coursedashboards.views.api.offering.course import CourseData
from coursedashboards.views.api.integration.course_cgpa import CourseCGPA
from coursedashboards.views.api.integration.course_fail_rate import \
    CourseFailRate
from coursedashboards.views.api.integration.course_majors import CourseMajors
from coursedashboards.views.index import index
from coursedashboards.views.page import user_login, logout

urlpatterns = [
    # Home
    url(r'^$', index, name='home'),
    url(r'^api/v1/course/past/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[a-z][a-z0-9]?)$',
        HistoricalCourseData.as_view(),
        name='historic_course_data'),
    url(r'^api/v1/course/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)$',
        CourseData.as_view(),
        name='course_data_for_term'),
    url(r'^api/v1/course/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)/'
        r'majors/(?P<num_majors>\d)$',
        CourseMajors.as_view(),
        name='course_majors'),
    url(r'^api/v1/course/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)/'
        r'fail_rate$',
        CourseFailRate.as_view(),
        name='course_fail_rate'),
    url(r'^api/v1/course/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)/'
        r'cgpa$',
        CourseCGPA.as_view(),
        name='course_cgpa'),
    url(r'^login', user_login),
    url(r'^logout', logout, name="coda_logout")
]
