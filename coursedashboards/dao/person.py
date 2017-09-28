import logging
from uw_sws.person import get_person_by_regid
from coursedashboards.util.retry import retry
from urllib3.exceptions import MaxRetryError


logger = logging.getLogger(__name__)


@retry(MaxRetryError, tries=5, delay=3, logger=logger)
def get_person_from_regid(regid):
    return get_person_by_regid(regid)
