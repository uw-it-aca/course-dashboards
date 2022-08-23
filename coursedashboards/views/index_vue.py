# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from coursedashboards.views.page import page
from coursedashboards.dao.message import get_persistent_messages


@login_required
def index_vue(request, year=None, quarter=None,
          curriculum_abbr=None, course_number=None,
          section_label=None, sections=None):

    context = {
        "year": None,
        "quarter": None,
        "curriculum": None,
        "course_number": None,
        "section_label": None,
        "sections": None,
    }
    print(context)

    context['messages'] = get_persistent_messages(params=context)

    return page(request, context, template='index_vue.html')
