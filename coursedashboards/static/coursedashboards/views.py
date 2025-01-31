# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.shortcuts import (
    render_to_response
)
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext


# HTTP Error 400
def bad_request(request):
    response = render_to_response(
        '400.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 400

    return response


# HTTP Error 403
def permission_denied(request):
    response = render_to_response(
        '403.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 403

    return response


# HTTP Error 404
def page_not_found(request):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 404

    return response


# HTTP Error 500
def server_error(request):
    response = render_to_response(
        '500.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 500

    return response
