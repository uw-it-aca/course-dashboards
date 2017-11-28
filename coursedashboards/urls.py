from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from coursedashboards.views.index import index
from coursedashboards.views.api.course import CourseData
from coursedashboards.views.api.historical import HistoricalCourseData
from coursedashboards.views.page import logout

urlpatterns = [
    # Home
    url(r'^$', index, name='home'),
    url(r'^api/v1/course/past/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[a-z][a-z0-9]?)$',
        login_required(HistoricalCourseData().run),
        name='historic_course_data'),
    url(r'^api/v1/course/(?i)(?P<year>\d{4})-'
        r'(?P<quarter>[A-Za-z]+)-'
        r'(?P<curriculum>[&% 0-9a-z]+)-'
        r'(?P<course_number>\d{3})-'
        r'(?P<section_id>[A-Za-z][A-Z0-9a-z]?)$',
        login_required(CourseData().run),
        name='course_data_for_term'),
    url(r'^logout', logout, name="coda_logout"),
]
