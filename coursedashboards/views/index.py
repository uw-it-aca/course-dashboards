# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from coursedashboards.views.page import page
from coursedashboards.dao.message import get_persistent_messages


@login_required
def index(request, year=None, quarter=None,
          curriculum_abbr=None, course_number=None,
          section_label=None, sections=None):

    context = {
        "year": year,
        "quarter": quarter,
        "curriculum": curriculum_abbr,
        "course_number": course_number,
        "section_label": section_label,
        "sections": sections,
    }

    context['messages'] = get_persistent_messages(params=context)

    return page(request, context, template='index.html')
