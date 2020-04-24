from .base_urls import *
from django.conf.urls import include, re_path


urlpatterns += [
    re_path(r'^', include('coursedashboards.urls')),
    re_path(r'^support', include('userservice.urls')),
    re_path(r'^logging', include('rc_django.urls')),
]
