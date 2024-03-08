# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from unittest import skipIf
from django.urls import reverse
from django.core.management import call_command
from django.test import TransactionTestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from userservice.user import UserServiceMiddleware
from coursedashboards.tests import get_user, get_user_pass

Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.PersistentRemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'
standard_test_override = override_settings(
    MIDDLEWARE=[Session,
                Common,
                CsrfView,
                Auth,
                RemoteUser,
                Message,
                XFrame,
                UserService],
    AUTHENTICATION_BACKENDS=[AUTH_BACKEND])


@standard_test_override
class CodaApiTest(TransactionTestCase):

    def setUp(self):
        """
        By default enforce_csrf_checks is False
        """
        self.client = Client()
        self.request = RequestFactory().get("/")
        self.middleware = UserServiceMiddleware()
        call_command('load_data_for_term', '--previous=4', '--next')

    def set_user(self, username):
        self.request.user = get_user(username)
        self.client.login(username=username,
                          password=get_user_pass(username))
        self.process_request()

    def process_request(self):
        self.request.session = self.client.session
        self.middleware.process_request(self.request)

    def get_response_by_reverse(self, url_reverse, *args, **kwargs):
        url = reverse(url_reverse, *args, **kwargs)
        return self.client.get(url)
