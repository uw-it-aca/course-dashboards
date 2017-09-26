from django.db import models


class Course(models.Model):
    curriculum = models.CharField(max_length=20)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)

    class Meta:
        db_table = "Course"
        unique_together = ('curriculum', 'course_number', 'section_id')

    def __str__(self):
        return "%s,%s/%s" % (
            self.curriculum, self.course_number, self.section_id)
