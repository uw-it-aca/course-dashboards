from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingGraduatedMajors(OfferingInfoView):

    def get_data(self, offering):
        return json.dumps(offering.get_graduated_majors())
