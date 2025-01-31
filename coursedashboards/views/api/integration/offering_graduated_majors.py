# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView


class OfferingGraduatedMajors(OfferingInfoView):

    def get_data(self, offering):
        return offering.get_graduated_majors()
