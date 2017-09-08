from django.db import models

from coursedashboards.models.course import Course
from user import User


class Major(models.Model):
    major = models.CharField(max_length=128,
                             db_index=True,
                             unique=True)


class StudentMajor(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    major = models.ForeignKey(Major,
                              on_delete=models.PROTECT)

    class Meta:
        db_table = 'StudentMajor'
        unique_together = ('user', 'major')


class CourseMajor(models.Model):
    major = models.ForeignKey(Major,
                              on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT,
                               db_index=True)
    count = models.IntegerField()

    class Meta:
        unique_together = ('major', 'course')

