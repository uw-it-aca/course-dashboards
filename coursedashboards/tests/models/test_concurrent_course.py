from unittest import TestCase

from unittest2 import skip, skipIf

from coursedashboards.models import Course, CourseOffering
from coursedashboards.models.course_offering import ConcurrentCourse


class TestConcurrentCourse(TestCase):

    def setUp(self):

        self.course = Course()
        self.course.curriculum = "PHYS"
        self.course.course_number = "122"
        self.course.section_id = "A"

        self.course2 = Course()
        self.course2.curriculum = "MATH"
        self.course2.course_number = "124"
        self.course2.section_id = "A"

        self.course_offering = CourseOffering()
        self.course_offering.course = self.course2
        self.course_offering.current_enrollment = 105

        self.concurrent_course = ConcurrentCourse()
        self.concurrent_course.course_offering = self.course_offering
        self.concurrent_course.concurrent_course = self.course
        self.concurrent_course.count = 23

    def test_json(self):
        course_json = self.concurrent_course.json_object()

        self.assertIn("number_students", course_json)
        self.assertIn("course", course_json)
        self.assertIn("percent_students", course_json)

        self.assertEqual(course_json["course"], str(self.course))
        self.assertEqual(course_json["percent_students"], 21.9)
        self.assertEqual(course_json["number_students"], 105)
