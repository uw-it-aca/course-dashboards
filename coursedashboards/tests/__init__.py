# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.models import User


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception:
        user = User.objects.create_user(username, password='pass')
        return user


def get_user_pass(username):
    return 'pass'
