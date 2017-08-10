import os
from django.conf import settings
from uw_sws.dao import SWS_DAO
from userservice.user import UserService
from coursedashboards.models import User


def get_netid_of_current_user():
    return UserService().get_user()


def is_using_file_dao():
    return SWS_DAO().get_implementation().is_mock()
