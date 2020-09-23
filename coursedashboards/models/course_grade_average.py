from django.db import models


class CourseGradeAverage(models.Model):
    curriculum = models.CharField(max_length=20)
    course_number = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = "CourseGradeAverage"

    def __str__(self):
        return "{}-{}: {}".format(
            self.curriculum, self.course_number, self.grade)
