from django.http import HttpResponse
from coursedashboards.views.api.integration.course_info import CourseInfoView
import json


class CourseCGPA(CourseInfoView):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):
        offering = self.get_offering(year, quarter, curriculum,
                                     course_number, section_id)

        if isinstance(offering, HttpResponse):
            return offering

        json_response = self.get_data(offering)
        return HttpResponse(json.dumps(json_response))

    def get_data(self, offering):
        json_obj = {}

        offering.set_json_cumulative_median(json_obj)

        return json_obj
