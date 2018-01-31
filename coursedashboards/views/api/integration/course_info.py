import json
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from coursedashboards.models import CourseOffering, Term, Course
from coursedashboards.views.api import CoDaAPI
from coursedashboards.views.error import _make_response, MYUW_DATA_ERROR


class CourseInfoView(CoDaAPI):
    """
    A superclass for handling individual data point/series retrievals about
    courses
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
