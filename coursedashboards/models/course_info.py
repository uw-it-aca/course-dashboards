from django.db import models

from coursedashboards.models import CourseOffering, Registration
from term import Term


class CourseInfo(models.Model):
    course = models.ForeignKey(CourseOffering)
    num_enrolled = models.IntegerField()
    num_repeating = models.IntegerField()
    median_gpa = models.FloatField()

    def __init__(self):

        repeats = 0

        registrations = Registration.objects.filter(term=self.course.term)

        for reg in registrations:
            if reg.is_repeat:
                repeats = repeats + 1

        self.num_repeating = repeats

    def json_object(self):
        json_object = {}

        return json_object
