from django.db import models
from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.models.course import Course


class Registration(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)
    grade = models.CharField(max_length=5, null=True)
    degree_level = models.IntegerField(default=1)
    credits = models.CharField(max_length=5, null=True)
    is_repeat = models.NullBooleanField()

    class Meta:
        db_table = 'Registration'
        unique_together = ('user', 'term', 'course')
