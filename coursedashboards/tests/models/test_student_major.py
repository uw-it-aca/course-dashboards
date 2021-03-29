# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

from coursedashboards.models import Term, StudentMajor


class TestStudentMajors(TestCase):

    def setUp(self):
        # create terms
        self.winter2016 = Term()
        self.winter2016.quarter = 'winter'
        self.winter2016.year = 2016
        self.autumn2017 = Term()
        self.autumn2017.quarter = 'autumn'
        self.autumn2017.year = 2017
        self.first_major = StudentMajor()
        self.first_major.term = self.winter2016
        self.second_major = StudentMajor()
        self.second_major.term = self.autumn2017

    def test_term_sort(self):
        sorted_majors = sorted([self.second_major, self.first_major])
