# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.apps import AppConfig
from restclients_core.dao import MockDAO
from os.path import join, abspath, dirname


class CoursedashboardsConfig(AppConfig):
    name = 'coursedashboards'

    def ready(self):
        MockDAO.register_mock_path(
            join(abspath(dirname(__file__)), "resources"))
