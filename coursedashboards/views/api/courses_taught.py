import json

from django.http import HttpResponse

from coursedashboards.views.api import CoDaAPI


class CoursesTaught(CoDaAPI):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):

        offering = self.get_offering(year, quarter, curriculum,
                                     course_number, section_id)

        if isinstance(offering, HttpResponse):
            return offering

        json_response = self.get_data(offering)
        return HttpResponse(json.dumps(json_response))

    def get_data(self, offering):

        return

