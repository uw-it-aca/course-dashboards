# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.views.api import UpStreamErrorException
from coursedashboards.dao.general_education import get_gen_ed_reqs_for_offering
import logging


logger = logging.getLogger(__name__)


class CourseGenEdData(CoDaEndpoint):
    def get_data(self, offering):
        try:
            return get_gen_ed_reqs_for_offering(offering)
        except Exception as ex:
            logger.exception("SWS Course: {}".format(ex))
            raise UpStreamErrorException()
