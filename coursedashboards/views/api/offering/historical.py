from coursedashboards.views.api.endpoint import CoDaEndpoint
import json


class HistoricalCourseData(CoDaEndpoint):

    def get_data(self, offering):
        return offering.past_offerings_json_object()
