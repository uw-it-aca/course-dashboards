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

        self.cse_142 = Course()
        self.cse_142.curriculum = "CSE"
        self.cse_142.section_id = "A"
        self.cse_142.course_number = 142
        self.cse_142.course_title = "COMPUTER PROGRAMMING I"
        self.cse_142.save()

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

        self.spring_cse = CourseOffering()
        self.spring_cse.course = self.cse_142
        self.spring_cse.term = self.spring
        self.spring_cse.current_enrollment = 3
        self.spring_cse.limit_estimate_enrollment = 25
        self.spring_cse.save()

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

        self.students[3].is_alum = True
        self.students[3].save()

        for x in range(0, 2):
            reg = Registration()
            reg.credits = 5
            reg.course = self.course
            reg.term = self.spring
            reg.user = self.students[x]
            reg.grade = 3.5
            self.registrations.append(reg)
            reg.save()

            reg = Registration()
            reg.credits = 5
            reg.course = self.cse_142
            reg.term = self.spring
            reg.user = self.students[x]
            reg.grade = 3.1
            self.registrations.append(reg)
            reg.save()

            major = StudentMajor()
            major.major = self.majors[0]
            major.user = self.students[x]
            major.term = self.spring
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
            major.term = self.winter
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
        major.term = self.winter
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
        major.term = self.winter
        self.student_majors.append(major)
        major.save()

        major = StudentMajor()
        major.major = self.majors[2]
        major.user = self.students[6]
        major.term = self.spring
        self.student_majors.append(major)
        major.save()

    def test_get_concurrent_courses(self):
        concurrent = self.spring_ess.concurrent_courses()
        self.assertEquals(len(concurrent), 1)
        self.assertEquals(concurrent[0]['number_students'], 2)

    def test_get_students(self):
        spring_students = self.spring_ess.get_students()
        self.assertEqual(len(spring_students), 3)

        winter_students = self.winter_ess.get_students()
        self.assertEqual(len(winter_students), 4)

    def test_majors(self):
        majors = self.winter_ess.get_majors()
        self.assertEqual(len(majors), 2)

    def test_graduated_majors(self):
        graduated_majors = self.winter_ess.get_graduated_majors()
        self.assertEquals(len(graduated_majors), 1)
        self.assertEquals(graduated_majors[0]['number_students'], 1)

    def test_student_cgpa(self):
        cgpa = self.winter_ess.get_cumulative_median_gpa()
        self.assertEquals(cgpa, 3.23)

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

        self.spring_cse.delete()
        self.cse_142.delete()
        self.spring_ess.delete()
        self.winter_ess.delete()
        self.course.delete()
        self.spring.delete()
        self.winter.delete()
