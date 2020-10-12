from memcached_clients import RestclientPymemcacheClient
import re

ONE_MINUTE = 60
ONE_HOUR = 60 * 60


class RestClientsCache(RestclientPymemcacheClient):
    """ A custom cache implementation for Course Dashboards """

    def get_cache_expiration_time(self, service, url, status=200):
        if "sws" == service:
            if re.match(r"^/student/v\d/term/\d{4}", url):
                return ONE_HOUR * 10
            if re.match(r"^/student/v\d/(?:enrollment|registration)", url):
                return ONE_HOUR * 2
            return ONE_HOUR

        if "pws" == service:
            return ONE_HOUR * 10

        if "gws" == service:
            return ONE_MINUTE * 2

        if "canvas" == service:
            if status == 200:
                return ONE_HOUR * 10
            return ONE_MINUTE * 5
