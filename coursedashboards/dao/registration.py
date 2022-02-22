# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from coursedashboards.util.retry import retry
from uw_sws.registration import get_active_registrations_by_section
from restclients_core.exceptions import DataFailureException
from urllib3.exceptions import MaxRetryError


logger = logging.getLogger(__name__)


@retry(MaxRetryError, tries=5, delay=3, logger=logger)
def get_active_registrations_for_section(section):
    try:
        return get_active_registrations_by_section(section)
    except DataFailureException as ex:
        if ex.status == 404:
            logger.info(" {}".format(ex))
        else:
            logger.error(" {}".format(ex))

    return []
