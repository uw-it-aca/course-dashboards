from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from coursedashboards.views.index import index


urlpatterns = [
    # Home
    url(r'^$', index, name='home')
]
