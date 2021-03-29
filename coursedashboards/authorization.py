# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from uw_saml.utils import is_member_of_group
from uw_pws import PWS
from coursedashboards.util.settings import (
    get_coda_admin_group, get_coda_override_group)


INVALID_STRING = ("Username not a valid netid (starts with a letter, "
                  "then 0-15 letters, _ or numbers)")
UPPERCASE = "Usernames must be all lowercase"
NO_USER = "No override user supplied"


def validate_netid(username):
    if len(username) == 0:
        return NO_USER

    if not PWS().valid_uwnetid(username):
        return INVALID_STRING

    return None


def can_override_user(request):
    return is_member_of_group(request, get_coda_override_group())


def can_proxy_restclient(request, service, url):
    return is_member_of_group(request, get_coda_admin_group())
