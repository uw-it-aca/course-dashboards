from rc_django.cache_implementation import TimedCache
from rc_django.models import CacheEntryTimed
import re


class RestClientsCache(TimedCache):
    """ A custom cache implementation for Course Dashboards """

    url_policies = {}
    url_policies["sws"] = (
        (re.compile(r"^/student/v5/term/current"), 60 * 60),
        (re.compile(r"^/student/v5/term/"), 60 * 60 * 10),
        (re.compile(r"^/student/v5/course/"), 60 * 60),
        (re.compile(r"^/student/v5/section"), 60 * 60),
    )
    url_policies["pws"] = (
        (re.compile(r"^/identity/v1/person/"), 60 * 60 * 10),
    )
    url_policies["gws"] = (
        (re.compile(r"^/group_sws/v2/group/"), 60 * 2),
    )

    def getCache(self, service, url, headers):
        cache_time = self.getCacheTime(service, url)
        if cache_time is not None:
            return self._response_from_cache(service, url, headers, cache_time)
        else:
            return None

    def processResponse(self, service, url, response):
        if self.getCacheTime(service, url) is not None:
            return self._process_response(service, url, response)
        else:
            return

    def getCacheTime(self, service, url):
        if service in RestClientsCache.url_policies:
            service_policies = RestClientsCache.url_policies[service]

            for policy in service_policies:
                pattern = policy[0]
                policy_cache_time = policy[1]

                if pattern.match(url):
                    return policy_cache_time
        return
