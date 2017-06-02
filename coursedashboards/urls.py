from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from coursedashboards.views import (
    HomeView,
    CoursePageView
)
from coursedashboards.views.index import index


urlpatterns = [
    # Home
    url(r'^course-page$', CoursePageView.as_view(), name='coursepage'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^$', RedirectView.as_view(url='/course-page')),
    #FOR TESTING DATA, WILL REMOVE
    url(r'^test$', index, name="login_test")
]
