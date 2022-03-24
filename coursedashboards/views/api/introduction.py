# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from coursedashboards.dao.user import get_current_user


class Introduction(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, netid):
        user = self.get_user(netid)
        return JsonResponse({
            'seen': user.intro_modal > 0,
            'version': user.intro_modal
        })

    def post(self, request, netid):
        user = self.get_user(netid)
        seen = request.data.get('seen')
        version = request.data.get('version')

        if seen:
            user.intro_modal = version
            #user.save()

        return JsonResponse({
            'seen': user.intro_modal > 0,
            'version': user.intro_modal
        })

    def get_user(self, netid):
        user = get_current_user()
        if netid != user.uwnetid:
            raise PermissionDenied()

        return user


