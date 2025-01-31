# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Course(models.Model):
    curriculum = models.CharField(max_length=20)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)
    course_title = models.CharField(max_length=64, default='')

    def sections(self):
        return Course.objects.filter(
            curriculum=self.curriculum,
            course_number=self.course_number).values_list(
                'id', flat=True).distinct()

    @property
    def ref(self):
        return "{}-{}".format(self.curriculum, self.course_number)

    class Meta:
        db_table = "Course"
        unique_together = ('curriculum', 'course_number', 'section_id')

    def __str__(self):
        return "{}-{}".format(self.ref, self.section_id)
