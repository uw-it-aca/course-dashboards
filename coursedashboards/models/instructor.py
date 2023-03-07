# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.models.course import Course


class InstructorManager(models.Manager):
    def instructed(self, instructor, term, course):
        return Instructor.objects.filter(
            user=instructor, term=term,
            course__curriculum=course.curriculum,
            course__course_number=course.course_number).values_list(
                'course__id', flat=True).distinct()


class Instructor(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)

    objects = InstructorManager()

    class Meta:
        db_table = 'Instructor'
        unique_together = ('user', 'term', 'course')
