from django.db import models

from coursedashboards.models.course_offering import CourseOffering
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
    course_offering = models.ForeignKey(CourseOffering,
                                        on_delete=models.PROTECT,
                                        db_index=True)
    count = models.IntegerField()

    class Meta:
        unique_together = ('major', 'course')

    def json_object(self):

        percentage = round(
            float(self.count) /
            float(self.course_offering.current_enrollment) * 100,
            2)
        return {
            'major': self.major.major,
            'number_students': self.count,
            'percent_students': percentage
        }
