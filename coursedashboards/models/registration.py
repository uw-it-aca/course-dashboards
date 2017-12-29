from django.db import models
from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.models.course import Course


class Registration(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             db_index=True)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT,
                               db_index=True)
    grade = models.CharField(max_length=5, null=True)
    credits = models.CharField(max_length=5, null=True)
    is_repeat = models.NullBooleanField()

    class Meta:
        db_table = 'Registration'
        unique_together = ('user', 'term', 'course')
        index_together = ('term', 'course')
