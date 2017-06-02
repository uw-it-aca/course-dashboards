import re
import logging
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.conf import settings
from coursedashboards.dao.term import get_current_quarter
from coursedashboards.dao.affiliation import get_all_affiliations
from coursedashboards.dao import get_netid_of_current_user


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
    print context
    return render(request, template, context)