from unittest import TestCase

from coursedashboards.models import Course, Term, CourseOffering


class TestCourseOffering(TestCase):

    def setUp(self):
        # create Course
        # create current and old CourseOffering
        # create three Students
        # create some historic registration/grade data
        # create a fail

        self.course = Course()
        self.course.curriculum = "ESS"
        self.course.section_id = "A"
        self.course.course_number = 102
        self.course.course_title = "Course Title"
        self.course.save()

        self.spring = Term()
        self.spring.quarter = Term.SPRING
        self.spring.year = 2016
        self.spring.save()

        self.winter = Term()
        self.winter.quarter = Term.WINTER
        self.winter.year = 2016
        self.winter.save()

        self.spring_ess = CourseOffering()


        pass

    def test_most_common_major(self):
        self.assertEqual(2, 3)

        # set majors

        # retrieve most common, then all majors

    def test_student_cgpa(self):

        self.assertEqual(2, 3)

        # Get student cgpa

    def test_historic_fail_rate(self):

        self.assertEqual(4, 5)

        # get historic fail rate
