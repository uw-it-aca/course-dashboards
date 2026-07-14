# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
import logging


logger = logging.getLogger(__name__)


def is_desktop(request):

    desktopapp = not request.is_mobile and not request.is_tablet

    return {
        'is_desktop': desktopapp
    }


class DumpHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"--- INCOMING REQUEST: {request.method} "
                    f"{request.path} (secure: "
                    f"{request.is_secure()}) ---")
        for key, value in request.headers.items():
            logger.info(f"Req-Header: {key}: {value}")

        return self.get_response(request)
