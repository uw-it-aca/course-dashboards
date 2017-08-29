from django.db import models
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
