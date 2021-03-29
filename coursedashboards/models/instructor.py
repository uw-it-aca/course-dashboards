# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.db import models
from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.models.course import Course


class Instructor(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)

    class Meta:
        db_table = 'Instructor'
        unique_together = ('user', 'term', 'course')
