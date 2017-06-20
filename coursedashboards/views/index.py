from coursedashboards.views.page import page
from coursedashboards.util.page_view import page_view


@page_view
def index(request, year=None, quarter=None, curriculum_abbr=None, course_number=None,section_label=None,sections=None):
    context = {
        "year": year,
        "quarter": quarter,
        "curriculum":curriculum_abbr,
        "course_number":course_number,
        "section_label":section_label,
        "sections":sections,
    }
    return page(request, context, template='index.html')