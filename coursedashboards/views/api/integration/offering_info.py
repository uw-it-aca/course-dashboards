# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from coursedashboards.views.api import CoDaAPI


class OfferingInfoView(CoDaAPI):
    """
    A superclass for handling individual data point/series retrievals about
    courses
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
