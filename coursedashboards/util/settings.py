# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.conf import settings


def get_coda_admin_group():
    return getattr(settings, "CODA_ADMIN_GROUP",
                   'u_acadev_coda_admins')


def get_coda_override_group():
    return getattr(settings, "CODA_OVERRIDE_GROUP",
                   'u_acadev_coda_admins')
