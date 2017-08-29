from django.db import models
from user import User
from term import Term
from course import Course


class Instructor(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)

    class Meta:
        db_table = 'Instructor'
        unique_together = ('user', 'term', 'course')
