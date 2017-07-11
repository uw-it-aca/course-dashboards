import hashlib
from datetime import timedelta
from datetime import datetime
from dateutil.parser import parse
from django.utils import timezone
from django.db import models
from django.utils import timezone

class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    uwregid = models.CharField(max_length=32,
                               null=True,
                               db_index=True,
                               unique=True)

    last_visit = models.DateTimeField(default=timezone.now)


class CourseMedianGPA(models.Model):
    section_id = models.CharField(max_length=100,
                                  db_index=True,
                                  unique=True)
    date_saved = models.DateTimeField()
    value = models.FloatField()

    @classmethod
    def get_cached(cls, section):
        label = section.section_label()
        limit = timezone.now() - timedelta(days=90)
        try:
            model = CourseMedianGPA.objects.get(section_id=label,
                                                date_saved__gte=limit)
            return model.value
        except CourseMedianGPA.DoesNotExist:
            return None

    @classmethod
    def save_value(cls, section, value):
        label = section.section_label()
        CourseMedianGPA.objects.filter(section_id=label).delete()

        try:
            v = CourseMedianGPA.objects.create(section_id=label,
                                               date_saved=timezone.now(),
                                               value=value)
        except Exception as ex:
            pass
