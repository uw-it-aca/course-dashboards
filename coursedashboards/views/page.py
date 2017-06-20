import json
import re
import logging
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from coursedashboards.dao.term import get_current_quarter
from coursedashboards.dao.affiliation import get_all_affiliations
from coursedashboards.dao import get_netid_of_current_user
from coursedashboards.dao.pws import get_person_of_current_user
from uw_sws.section import get_sections_by_instructor_and_term
from coursedashboards.dao.instructor_schedule import get_instructor_schedule_by_term


#logger = logging.getLogger(__name__)

def page(request,
         context={},
         template='course-page.html'):
    #timer = Timer()
    netid = get_netid_of_current_user()
    if not netid:
        #log_invalid_netid_response(logger, timer)
        return "nope"#invalid_session()
    context["user"] = {
        "netid": netid,
        "session_key": request.session.session_key,
     }

    context["home_url"] = "/"
    context["err"] = None
    context["user"]["affiliations"] = get_all_affiliations(request)
    #print context["user"]["affiliations"]

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
    
    #adding below so can get instructors schedule
    person = get_person_of_current_user()
    
    #WORKS ONLY WITH bill100 - NEED ERROR HANDLING WHEN NO COURSES
    sections = get_sections_by_instructor_and_term(person, cur_term)
    context["sections"] = []
    for section in sections:
        cur_section = section.json_data()
        context["sections"].append({
            'curriculum':cur_section['curriculum_abbr'],
            'course_number':cur_section['course_number'],
            'section_label':cur_section['section_label'],
            'section_id':cur_section['section_id']
        })
        print cur_section
    context["sections"] = json.dumps(list(context["sections"]), cls=DjangoJSONEncoder)
    
    
    return render(request, template, context)