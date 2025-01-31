# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from coursedashboards.dao.pds import get_students_by_uwnetids


class TestPDS(TestCase):
    databases = '__all__'
    fixtures = ['person.json', 'employee.json', 'term.json', 'major.json',
                'student.json', 'adviser.json', 'transfer.json',
                'transcript.json', 'hold.json', 'degree.json', 'sport.json']

    def test_get_students_by_uwnetids(self):
        queryset = get_students_by_uwnetids(['javerage', 'jbothell'])
        data = list(queryset)

        self.assertEqual(len(data), 2)

        data1 = data[0]
        self.assertEqual(data1['person__uwnetid'], 'javerage')
        self.assertEqual(data1['application_type_code'], '1')
        self.assertTrue(data1['disability_ind'])
        self.assertEqual(data1['special_program_code'], '0')
        self.assertEqual(data1['latest_transcript']['scholarship_type'], 0)
