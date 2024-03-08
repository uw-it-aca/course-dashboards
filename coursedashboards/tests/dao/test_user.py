# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from coursedashboards.models import User
from coursedashboards.dao.pws import get_person_by_netid
from coursedashboards.dao.person import get_person_from_regid
from coursedashboards.dao.user import _user_from_person, user_from_person


class TestGetUser(TestCase):

    def test_get_alum_user(self):
        bill = get_person_from_regid("1A029BDC42DF11D9ABA3000629C31437")
        user = user_from_person(bill)

        self.assertTrue(user.is_alum)

    def test_netid_change(self):
        bill = get_person_by_netid('bill')
        user = _user_from_person(bill)

        # change netid
        bill.prior_uwnetids.append('bill')
        bill.uwnetid = 'bob'
        user = user_from_person(bill)

        self.assertEqual(user.uwnetid, 'bob')
        self.assertEqual(len(User.objects.all()), 1)

    def test_regid_change(self):
        bill = get_person_by_netid('bill')
        user = _user_from_person(bill)

        # change regid
        bill.prior_uwregids.append(bill.uwregid)
        bill.uwregid = 'ABCD1234ABCD1234ABCD1234ABCD1234'
        user = user_from_person(bill)

        self.assertEqual(user.uwregid, 'ABCD1234ABCD1234ABCD1234ABCD1234')
        self.assertEqual(len(User.objects.all()), 1)

    def test_regid_netid_change(self):
        bill = get_person_by_netid('bill')
        new_netid = 'bob'
        new_regid = 'ABCD1234ABCD1234ABCD1234ABCD1234'
        prior_netid = bill.uwnetid
        prior_regid = bill.uwregid

        bill.uwnetid = prior_netid
        bill.uwregid = new_regid
        bill.prior_uwregids = [prior_regid]
        user = _user_from_person(bill)

        bill.uwnetid = new_netid
        bill.prior_uwnetids = [prior_netid]
        bill.uwregid = prior_regid
        bill.prior_uwregids = []
        user = _user_from_person(bill)

        self.assertEqual(len(User.objects.all()), 2)

        bill.uwnetid = new_netid
        bill.prior_uwnetids = [prior_netid]
        bill.uwregid = new_regid
        bill.prior_uwregids = [prior_regid]
        user = user_from_person(bill)

        self.assertEqual(user.uwnetid, new_netid)
        self.assertEqual(user.uwregid, new_regid)

        self.assertEqual(len(User.objects.all()), 2)

        new_user = User.objects.get(uwnetid=new_netid)
        self.assertEqual(new_user.uwregid, new_regid)

        prior_user = User.objects.get(uwnetid=prior_netid)
        self.assertEqual(prior_user.uwregid, prior_regid)
