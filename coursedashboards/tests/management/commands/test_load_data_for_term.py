# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.core.management import call_command
from coursedashboards.models import CourseOffering, Registration


class TestLoadDataForTerm(TestCase):
    def test_load_data_for_term(self):
        call_command('load_data_for_term', '--next')

        self.assertEquals(CourseOffering.objects.all().count(), 6)
        self.assertEquals(Registration.objects.all().count(), 398)
