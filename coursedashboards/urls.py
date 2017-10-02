from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from coursedashboards.views.index import index
from coursedashboards.views.api.course import course
from coursedashboards.views.api.historical import historical


urlpatterns = [
    # Home
    url(r'^$', index, name='home'),
    url(r'^(?i)(?<year>\d{4})-(?<quarter>(winter|spring|summer|autumn))'
        r'-(?<curriculum>[a-z \&]+-(?<course>\d{3})-'
        r'-(?<section>[a-z]{,2})$', course, name='current_course'),
    url(r'^(?i)(?<year>\d{4})-(?<quarter>(winter|spring|summer|autumn))'
        r'-(?<curriculum>[a-z \&]+-(?<course>\d{3})-'
        r'-(?<section>[a-z]{,2})$', historical, name='historical_course'),
]
