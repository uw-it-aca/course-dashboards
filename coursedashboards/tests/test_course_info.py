from unittest import TestCase

from coursedashboards.models import Registration, Course, CourseOffering
from coursedashboards.models.course_info import CourseInfo


class TestCourseInfo(TestCase):

    def test_num_repeating(self):

        course = CourseOffering()

        for x in range(0, 12):
            reg = Registration()
            reg.is_repeat = x >= 5
            reg.course = course

        course_info = CourseInfo(course)

        self.assertEqual(course_info.num_repeating, 6)
