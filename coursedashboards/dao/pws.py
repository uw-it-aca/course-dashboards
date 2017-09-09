"""
This module encapsulates the interactions with the uw_pws,
provides information of the current user
"""

import logging
from uw_pws import PWS
from coursedashboards.dao import get_netid_of_current_user

logger = logging.getLogger(__name__)


def get_person_by_netid(netid):
    """
    Retrieve person data using the given netid
    """
    return PWS().get_person_by_netid(netid)


def get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    return get_person_by_netid(get_netid_of_current_user())
