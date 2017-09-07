from django.db import models
from user import User
from term import Term
from course import Course


class Registration(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)
    grade = models.CharField(max_length=5, null=True)
    is_repeat = models.NullBooleanField()

    class Meta:
        db_table = 'Registration'
        unique_together = ('user', 'term', 'course')
