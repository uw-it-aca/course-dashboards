from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingCGPA(OfferingInfoView):

    def get_data(self, offering):
        json_obj = {}

        offering.set_json_cumulative_median(json_obj)

        return json.dumps(json_obj)
