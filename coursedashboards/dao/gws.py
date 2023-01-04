# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from django.conf import settings
from uw_gws import GWS


def get_effective_members(group_name):
    return GWS().get_effective_members(group_name)


def is_in_admin_group(group_key):
    user_service = UserService()
    user_service.get_user()
    # Do the group auth here.

    if not hasattr(settings, group_key):
        print("You must have a group defined as your admin group.")
        print('Configure that using {}="foo_group"'.format(group_key))
        raise Exception("Missing {} in settings".format(group_key))

    actual_user = user_service.get_original_user()
    if not actual_user:
        raise Exception("No user in session")

    group_name = getattr(settings, group_key)
    return GWS().is_member_of_group(actual_user, group_name)
