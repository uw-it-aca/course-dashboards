# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from coursedashboards.views.api.endpoint import CoDaEndpoint


class HistoricalCourseData(CoDaEndpoint):

    def get_data(self, offering):
        return offering.past_offerings_json_object()
