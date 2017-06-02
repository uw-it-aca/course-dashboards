import re
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.conf import settings
from coursedashboards.dao.term import get_current_quarter
from coursedashboards.dao.affiliation import get_all_affiliations
from coursedashboards.dao import get_netid_of_current_user

class TestMe():
    def get_netid():
        return get_netid_of_current_user
        