# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingFailRate(OfferingInfoView):

    def get_data(self, offering):
        response = {}

        offering.set_fail_rate(response)

        return response
