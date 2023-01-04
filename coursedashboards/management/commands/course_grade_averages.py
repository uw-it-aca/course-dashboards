# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from coursedashboards.models import Course, Registration, CourseGradeAverage
from statistics import mean
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populate CourseGradeAverage table"

    def handle(self, *args, **options):
        courses = {}
        for c in Course.objects.all():
            if c.curriculum in courses:
                if c.course_number in courses[c.curriculum]:
                    courses[c.curriculum][
                        c.course_number] = self._running_average(
                            c, courses[c.curriculum][c.course_number])
                else:
                    courses[c.curriculum][
                        c.course_number] = self._running_average(c)
            else:
                courses[c.curriculum] = {
                    c.course_number: self._running_average(c)
                }

        for c in courses:
            for n in courses[c]:
                CourseGradeAverage.objects.update_or_create(
                    curriculum=c, course_number=n,
                    defaults={
                        'grade': "{:.2f}".format(courses[c][n]['mean'])
                    })

    def _running_average(self, course, running=None):
        grades = []
        for g in Registration.objects.filter(
                course=course).values_list('grade', flat=True):
            try:
                grades.append(float(g))
            except ValueError:
                pass

        N = len(grades)
        m = mean(grades) if N > 0 else 0

        if running:
            N_sum = N + running['N']
            if N_sum > 0:
                return {
                    'mean': (
                        (N * m) + (running['N'] * running['mean'])) / N_sum,
                    'N': N_sum
                }

        return {
            'mean': m,
            'N': N
        }
