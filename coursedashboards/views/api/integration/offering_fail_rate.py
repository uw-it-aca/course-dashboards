from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingFailRate(OfferingInfoView):

    def get_data(self, offering):
        response = {}

        offering.set_fail_rate(response)

        return response
