# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingCGPA(OfferingInfoView):

    def get_data(self, offering):
        json_obj = {}

        offering.set_json_cumulative_median(json_obj)

        return json_obj
