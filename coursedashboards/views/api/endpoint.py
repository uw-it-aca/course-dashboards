# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import json
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication, \
    SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from coursedashboards.models import CourseOffering, Term, Course
from coursedashboards.views.api import CoDaAPI
from coursedashboards.views.error import _make_response, MYUW_DATA_ERROR


class CoDaEndpoint(CoDaAPI):
    """
    A superclass for handling clientside data retrieval (requires login)
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
