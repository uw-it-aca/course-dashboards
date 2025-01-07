# Copyright 2025 UW-IT, University of Washington
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
    databases = '__all__'
    fixtures = [
        'initial_data/term.json',
        'initial_data/user.json',
        'initial_data/course.json',
        'initial_data/course_offering.json',
        'initial_data/instructor.json',
        'initial_data/major.json',
        'initial_data/registration.json',
        'initial_data/student_major.json',
        'uw_person/person.json',
        'uw_person/student.json',
        'person.json',
        'term.json',
        'major.json',
        'student.json',
        'transcript.json']

    def setUp(self):
        """
        By default enforce_csrf_checks is False
        """
        self.client = Client()
        self.request = RequestFactory().get("/")
        self.middleware = UserServiceMiddleware()
#        call_command('initialize_db')

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
