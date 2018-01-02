
import json
from django.http import HttpResponse
from coursedashboards.models import Term, Course, CourseOffering
from coursedashboards.views.rest_dispatch import RESTDispatch
from coursedashboards.views.error import data_not_found, data_error


class CourseData(RESTDispatch):
    """
    Performs actions on /api/v1/course/yyyy-quarter-curric-course-section
    """
    def GET(self, request, year, quarter,
            curriculum, course_number, section_id):
        try:
            term = Term.objects.get(year=year, quarter=quarter.lower())
            course = Course.objects.get(curriculum=curriculum.upper(),
                                        course_number=course_number,
                                        section_id=section_id.upper())
            offering = CourseOffering.objects.get(term=term, course=course)

            if offering.current_enrollment <= 5:
                return HttpResponse(json.dumps(offering.base_json_object()))

            return HttpResponse(json.dumps(offering.json_object()))

        except (Term.DoesNotExist, Course.DoesNotExist,
                CourseOffering.DoesNotExist):
            return data_not_found()

        return data_error()
