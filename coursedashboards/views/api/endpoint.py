# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from coursedashboards.views.api import CoDaAPI


class CoDaEndpoint(CoDaAPI):
    """
    A superclass for handling clientside data retrieval (requires login)
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
