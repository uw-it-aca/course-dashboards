import logging
from uw_sws.registration import get_active_registrations_by_section
from restclients_core.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def get_active_registrations_for_section(section):
    try:
        return get_active_registrations_by_section(section)
    except DataFailureException as ex:
        if ex.status == 404:
            logger.info(" %s" % ex)
        else:
            logger.error(" %s" % ex)

    return []
