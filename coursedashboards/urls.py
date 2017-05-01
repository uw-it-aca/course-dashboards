from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from coursedashboards.views import (
    HomeView,
    CoursePageView
)


urlpatterns = [
    # Home
    url(r'^$', RedirectView.as_view(url='/major-gpa')),
    url(r'^course-page$', CoursePageView.as_view(), name='coursepage'),
    url(r'^$', HomeView.as_view(), name='home'),

]
