# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.shortcuts import render
from coursedashboards.dao.user import get_current_user
from coursedashboards.dao.term import (
    get_current_coda_term, get_given_and_previous_quarters,
    get_term_from_quarter_string, get_term_after_current)
from coursedashboards.dao.exceptions import (
    MissingNetIDException, NoTermAfterCurrent)
from coursedashboards.models import Term, Instructor, CourseOffering
from django.contrib.auth import logout as django_logout


LOGOUT_URL = "/user_logout"
HISTORIC_TERM_COUNT = 12


def page(request,
         context={},
         template='course-page.html'):
    try:
        user = get_current_user()
        context["user"] = {
            "netid": user.uwnetid,
            "session_key": request.session.session_key,
            "intro_modal": user.intro_modal
        }
    except MissingNetIDException:
        # below is placeholder if login fails...
        # should log and return something useful
        # log_invalid_netid_response(logger, timer)
        return "nope"  # insvalid_session()

    context["home_url"] = "/"
    context["err"] = None
    if ('year' in context and context['year'] and
            'quarter' in context and context['quarter']):
        cur_term, created = Term.objects.get_or_create(
            year=context['year'], quarter=context['quarter'])
    else:
        cur_term = get_current_coda_term(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter

    try:
        sections = []
        historical = {}

        for sws_term in get_page_terms(cur_term.sws_label):
            term, created = Term.objects.get_or_create(
                year=sws_term.year, quarter=sws_term.quarter)

            courses = Instructor.objects.filter(
                user=user, term=term).values_list('course_id', flat=True)
            offerings = CourseOffering.objects.filter(
                course_id__in=list(courses), term=term)

            for offering in offerings:
                course_label = str(offering)
                sections.append(offering.brief_json_object())
                historical[course_label] = {}

        context['sections'] = json.dumps(sections, cls=DjangoJSONEncoder)
        context['historic_sections'] = json.dumps(
            historical, cls=DjangoJSONEncoder)

        if len(sections) == 0:
            context['no_courses'] = True

    except Instructor.DoesNotExist:
        context['no_courses'] = True

    return render(request, template, context)


def get_page_terms(cur_term_name):
    terms = get_given_and_previous_quarters(
        cur_term_name, HISTORIC_TERM_COUNT + 1)

    try:
        cur_term = get_term_from_quarter_string(cur_term_name)
        terms.append(get_term_after_current(cur_term))
    except NoTermAfterCurrent:
        pass

    return terms


def user_login(request):
    return HttpResponseRedirect(request.GET.get('next', '/'))


def logout(request):
    # Expires current myuw session
    django_logout(request)

    # Redirects to weblogin logout page
    return HttpResponseRedirect(LOGOUT_URL)
