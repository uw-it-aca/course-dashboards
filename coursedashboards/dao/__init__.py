from uw_sws.dao import SWS_DAO
from userservice.user import UserService


def get_netid_of_current_user():
    return UserService().get_user()


def is_using_file_dao():
    return SWS_DAO().get_implementation().is_mock()
