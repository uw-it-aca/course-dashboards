# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint


class CourseData(CoDaEndpoint):

    def get_data(self, offering):
        if offering.current_enrollment <= 5:
            return offering.base_json_object()

        return offering.json_object()
