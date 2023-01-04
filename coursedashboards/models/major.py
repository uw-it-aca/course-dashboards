# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models

from coursedashboards.models.term import Term
from coursedashboards.models.user import User


class Major(models.Model):
    major = models.CharField(max_length=128,
                             db_index=True)
    degree_level = models.IntegerField(default=0)


class StudentMajor(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    major = models.ForeignKey(Major,
                              on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             null=True,
                             on_delete=models.PROTECT)

    class Meta:
        db_table = 'StudentMajor'
        unique_together = ('user', 'major', 'term')

    def __lt__(self, other):
        return self.term < other.term

    @staticmethod
    def sort_by_term(first, other):
        return first.term.compare_terms(first.term, other.term)
