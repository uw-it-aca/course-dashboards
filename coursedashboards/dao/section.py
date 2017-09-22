import logging
from uw_sws.section import get_changed_sections_by_term, get_section_by_url
from coursedashboards.util.retry import retry
from urllib3.exceptions import MaxRetryError

logger = logging.getLogger(__name__)


@retry(MaxRetryError, tries=5, delay=3, logger=logger)
def get_changed_sections(changed_since, term, **params):
    return get_changed_sections_by_term(changed_since, term, **params)


@retry(MaxRetryError, tries=5, delay=3, logger=logger)
def get_section_from_url(url):
    return get_section_by_url(url)
