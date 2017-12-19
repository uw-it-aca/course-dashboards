import json
from django.http import HttpResponse
from coursedashboards.models import Term, Course, CourseOffering
from coursedashboards.views.api import CoDaAPI
from coursedashboards.views.rest_dispatch import RESTDispatch
from coursedashboards.views.error import data_not_found, data_error


class CourseData(CoDaAPI):
    """
    Performs actions on /api/v1/course/yyyy-quarter-curric-course-section
    """

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):
        try:
            offering = self.get_offering(year, quarter, curriculum,
                                         course_number, section_id)
        except Term.DoesNotExist:
            return self.term_not_found()
        except Course.DoesNotExist:
            return self.course_not_found()
        except CourseOffering.DoesNotExist:
            return self.course_offering_not_found()

        json_response = self.get_data(offering)
        return HttpResponse(json.dumps(json_response))

    def get_data(self, offering):
        if offering.current_enrollment <= 5:
            return offering.base_json_object()

        return offering.json_object()
