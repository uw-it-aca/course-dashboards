from django.urls import include, re_path


urlpatterns = [
    re_path(r'^saml/', include('uw_saml.urls')),
    re_path(r'^support', include('userservice.urls')),
    re_path(r'^logging', include('django_client_logger.urls')),
    re_path(r'^logging', include('rc_django.urls')),
    re_path(r'^', include('coursedashboards.urls')),
]
