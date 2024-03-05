# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the interactions with the uw_pws,
provides information of the current user
"""

import logging
from uw_pws import PWS
from coursedashboards.dao.exceptions import MissingNetIDException
from coursedashboards.util.retry import retry
from coursedashboards.dao import get_netid_of_current_user
from urllib3.exceptions import MaxRetryError


logger = logging.getLogger(__name__)


@retry(MaxRetryError, tries=5, delay=3, logger=logger)
def get_person_by_netid(netid):
    """
    Retrieve person data using the given netid
    """
    return PWS().get_person_by_netid(netid)


def get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    netid = get_netid_of_current_user()
    if not netid:
        raise MissingNetIDException()

    return get_person_by_netid(netid)
