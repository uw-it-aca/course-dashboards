# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings


def is_desktop(request):

    desktopapp = not request.is_mobile and not request.is_tablet

    return {
        'is_desktop': desktopapp
    }

def google_analytics(request):

    ga_key = getattr(settings, "GOOGLE_ANALYTICS_KEY", " ")
    return {"google_analytics": ga_key}


def django_debug(request):

    django_debug = getattr(settings, "DEBUG", False)
    return {"django_debug": django_debug}
