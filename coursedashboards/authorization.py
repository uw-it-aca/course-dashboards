from django.conf import settings
from uw_saml.utils import is_member_of_group


def can_override_user(request):
    return is_member_of_group(request, settings.CODA_ADMIN_GROUP)


def can_proxy_restclient(request, service, url):
    return is_member_of_group(request, settings.CODA_ADMIN_GROUP)


def can_manage_persistent_messages(request):
    return is_member_of_group(request, settings.CODA_ADMIN_GROUP)
