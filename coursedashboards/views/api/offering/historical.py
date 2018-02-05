from django.http import HttpResponse
from coursedashboards.views.api.endpoint import CoDaEndpoint
import json


class HistoricalCourseData(CoDaEndpoint):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):

        offering = self.get_offering(year, quarter, curriculum,
                                     course_number, section_id)

        if isinstance(offering, HttpResponse):
            return offering

        json_response = self.get_data(offering)
        return HttpResponse(json_response)

    def get_data(self, offering):
        return json.dumps(offering.past_offerings_json_object())
