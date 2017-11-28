from unittest import TestCase

from django.test import TransactionTestCase

from coursedashboards.models import Course, Term, CourseOffering, User, \
    Registration, Major, StudentMajor


class TestCourseOffering(TransactionTestCase):

    def setUp(self):
        self.course = Course()
        self.course.curriculum = "ESS"
        self.course.section_id = "A"
        self.course.course_number = 107
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
        self.spring_ess.course = self.course
        self.spring_ess.term = self.spring
        self.spring_ess.current_enrollment = 24
        self.spring_ess.limit_estimate_enrollment = 25
        self.spring_ess.save()

        self.winter_ess = CourseOffering()
        self.winter_ess.course = self.course
        self.winter_ess.term = self.winter
        self.winter_ess.current_enrollment = 25
        self.winter_ess.limit_estimate_enrollment = 25
        self.winter_ess.save()

        self.majors = []

        philosophy = Major()
        philosophy.degree_level = 1
        philosophy.major = "Philosophy"
        self.majors.append(philosophy)

        computer_science = Major()
        computer_science.degree_level = 1
        computer_science.major = "Computer Science"
        self.majors.append(computer_science)

        pre_science = Major()
        pre_science.degree_level = 0
        pre_science.major = "Pre Science"
        self.majors.append(pre_science)

        for major in self.majors:
            major.save()

        self.students = []
        self.registrations = []
        self.student_majors = []

        for x in range(0, 7):
            user = User()
            user.uwnetid = "netid" + str(x)
            user.save()
            self.students.append(user)

        for x in range(0, 2):
            reg = Registration()
            reg.credits = 5
            reg.course = self.course
            reg.term = self.spring
            reg.user = self.students[x]
            reg.grade = 3.5
            self.registrations.append(reg)
            reg.save()

            major = StudentMajor()
            major.major = self.majors[0]
            major.user = self.students[x]
            self.student_majors.append(major)
            major.save()

        for x in range(3, 5):
            reg = Registration()
            reg.credits = 5
            reg.course = self.course
            reg.term = self.winter
            reg.user = self.students[x]
            reg.grade = 3.5
            self.registrations.append(reg)
            reg.save()

            major = StudentMajor()
            major.major = self.majors[1]
            major.user = self.students[x]
            self.student_majors.append(major)
            major.save()

        reg = Registration()
        reg.credits = 5
        reg.course = self.course
        reg.term = self.winter
        reg.user = self.students[5]
        reg.grade = 0.7
        self.registrations.append(reg)
        reg.save()

        major = StudentMajor()
        major.major = self.majors[2]
        major.user = self.students[5]
        self.student_majors.append(major)
        major.save()

        reg = Registration()
        reg.credits = 5
        reg.course = self.course
        reg.term = self.spring
        reg.user = self.students[6]
        reg.grade = 3.5
        reg.is_repeat = True
        self.registrations.append(reg)
        reg.save()

        reg = Registration()
        reg.credits = 5
        reg.course = self.course
        reg.term = self.winter
        reg.user = self.students[6]
        reg.grade = 2.4
        reg.is_repeat = False
        self.registrations.append(reg)
        reg.save()

        major = StudentMajor()
        major.major = self.majors[2]
        major.user = self.students[6]
        self.student_majors.append(major)
        major.save()

    def test_majors(self):
        majors = self.winter_ess.get_majors()

    def test_graduated_majors(self):
        graduated_majors = self.winter_ess.get_graduated_majors()

    def test_student_cgpa(self):
        cgpa = self.winter_ess.get_cumulative_median_gpa()
        print cgpa

    def test_historic_fail_rate(self):
        fail_rate = self.spring_ess.get_fail_rate()
        self.assertEqual(fail_rate, 1 / 7)

    def tearDown(self):
        for stumaj in self.student_majors:
            stumaj.delete()

        for reg in self.registrations:
            reg.delete()

        for student in self.students:
            student.delete()

        for major in self.majors:
            major.delete()

        self.spring_ess.delete()
        self.winter_ess.delete()
        self.course.delete()
        self.spring.delete()
        self.winter.delete()
