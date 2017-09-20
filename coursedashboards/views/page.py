import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from coursedashboards.dao.user import get_current_user
from coursedashboards.dao.term import get_current_coda_term
from coursedashboards.dao.exceptions import MissingNetIDException
from coursedashboards.models import Instructor, CourseOffering


def page(request,
         context={},
         template='course-page.html'):
    try:
        user = get_current_user()
        context["user"] = {
            "netid": user.uwnetid,
            "session_key": request.session.session_key,
        }
    except MissingNetIDException:
        # below is placeholder if login fails...
        # should log and return something useful
        # log_invalid_netid_response(logger, timer)
        return "nope"  # insvalid_session()

    context["home_url"] = "/"
    context["err"] = None
    if ('year' not in context or context['year'] is None or
            'quarter' not in context and context['quarter'] is None):
        cur_term = get_current_coda_term(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass

    context['sections'] = []
    try:
        courses = Instructor.objects.filter(
            user=user, term=cur_term).values_list('course', flat=True)
        offerings = CourseOffering.objects.filter(
            course=courses, term=cur_term)

        context['no_courses'] = (len(offerings) == 0)
        sections = []
        for offering in offerings:
            sections.append(offering.json_object())

        context['sections'] = json.dumps(sections, cls=DjangoJSONEncoder)

    except Instructor.DoesNotExist:
        context['no_courses'] = True

    return render(request, template, context)
