# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from django.db import models


class CourseGradeAverage(models.Model):
    curriculum = models.CharField(max_length=20)
    course_number = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = "CourseGradeAverage"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=['curriculum', 'course_number'])
        ]

    def __str__(self):
        return f"{self.curriculum}-{self.course_number}: {self.grade}"
