# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging

from coursedashboards.dao.general_education import get_gen_ed_reqs_for_offering
from coursedashboards.views.api import UpStreamErrorException
from coursedashboards.views.api.endpoint import CoDaEndpoint

logger = logging.getLogger(__name__)


class CourseGenEdData(CoDaEndpoint):
    def get_data(self, offering):
        try:
            return get_gen_ed_reqs_for_offering(offering)
        except Exception:
            logger.exception(f"GenEdData: Error retrieving gen ed data for {offering}")
            raise UpStreamErrorException()
