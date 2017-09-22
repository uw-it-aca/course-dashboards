from django.db import models

from coursedashboards.models.term import Term


class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    uwregid = models.CharField(max_length=32,
                               null=True,
                               db_index=True,
                               unique=True)
    last_enrolled = models.ForeignKey(Term,
                                      null=True,
                                      on_delete=models.PROTECT)

    display_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=255, null=True)


class QuarterGPA(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    gpa = models.FloatField()
    credits = models.IntegerField()
