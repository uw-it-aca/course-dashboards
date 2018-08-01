import re
from coursedashboards.util.settings import get_coda_override_group
from uw_saml.utils import is_member_of_group


INVALID_STRING = ("Username not a valid netid (starts with a letter, "
                  "then 0-15 letters, _ or numbers)")
UPPERCASE = "Usernames must be all lowercase"
NO_USER = "No override user supplied"


def validate(username):
    if len(username) == 0:
        return NO_USER

    if username != username.lower():
        return UPPERCASE

    re_personal_netid = re.compile(r'^[a-z][_a-z0-9]{0,15}$', re.I)
    if not re_personal_netid.match(username):
        return INVALID_STRING

    return None


def can_override_user(request):
    """
    Return True if the original user has impersonate permission
    """
    return is_member_of_group(request, get_coda_override_group())
