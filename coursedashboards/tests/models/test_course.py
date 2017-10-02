from django.test import TestCase
from django.conf import settings
from coursedashboards.models import Course


class TestCourse(TestCase):

    def setUp(self):

        self.course = Course()
        self.course.curriculum = "PHYS"
        self.course.course_number = "122"
        self.course.section_id = "A"

    def test_str(self):
        self.assertEqual(str(self.course), "PHYS-122-A")
