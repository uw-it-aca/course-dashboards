# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.template import Library
from coursedashboards.dao.gws import is_in_admin_group


register = Library()


@register.simple_tag(takes_context=True)
def add_admin_checks(context):
    context['is_overrider'] = is_in_admin_group('USERSERVICE_ADMIN_GROUP')
    context['is_rest_browser'] = is_in_admin_group('RESTCLIENTS_ADMIN_GROUP')
    return ''
