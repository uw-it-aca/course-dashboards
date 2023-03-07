# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class CourseManager(models.Manager):
    def sections(self, course):
        course_ids = [c.id for c in Course.objects.filter(
            curriculum=course.curriculum, course_number=course.course_number)]
        return [*set(course_ids)]


class Course(models.Model):
    curriculum = models.CharField(max_length=20)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)
    course_title = models.CharField(max_length=64, default='')

    objects = CourseManager()

    @property
    def ref(self):
        return "{}-{}".format(self.curriculum, self.course_number)

    class Meta:
        db_table = "Course"
        unique_together = ('curriculum', 'course_number', 'section_id')

    def __str__(self):
        return "{}-{}".format(self.ref, self.section_id)
