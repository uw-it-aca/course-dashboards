from unittest2 import TestCase

from coursedashboards.dao.person import get_person_from_regid
from coursedashboards.dao.user import user_from_person


class TestGetUser(TestCase):

    def test_get_alum_user(self):
        bill = get_person_from_regid("1A029BDC42DF11D9ABA3000629C31437")
        user = user_from_person(bill)

        self.assertTrue(user.is_alum)
