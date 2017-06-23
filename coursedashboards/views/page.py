import re
import logging
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.conf import settings
from coursedashboards.dao import get_netid_of_current_user
from coursedashboards.dao.pws import get_person_of_current_user
from coursedashboards.dao.term import get_current_quarter
from coursedashboards.dao.section import create_sections_context, get_instructor_current_sections

def page(request,
         context={},
         template='course-page.html'):
    netid = get_netid_of_current_user()
    #below is placeholder if login fails... should log and return something useful
    if not netid:
        #log_invalid_netid_response(logger, timer)
        return "nope"#invalid_session()
    context["user"] = {
        "netid": netid,
        "session_key": request.session.session_key,
     }

    context["home_url"] = "/"
    context["err"] = None
    if ('year' not in context or context['year'] is None or
            'quarter' not in context and context['quarter'] is None):
        cur_term = get_current_quarter(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    
    person = get_person_of_current_user()
    
    #WORKS ONLY WITH bill100 - NEED ERROR HANDLING WHEN NO COURSES
    #currently getting ALL data for EVERY section being taught...perhaps should only pull data when needed?
    sections = get_instructor_current_sections(person, cur_term)
    context["sections"] = create_sections_context(sections,cur_term)
    
    return render(request, template, context)

