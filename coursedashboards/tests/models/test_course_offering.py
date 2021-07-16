from unittest import TestCase
from django.test import TransactionTestCase
from coursedashboards.models import Course, Term, CourseOffering, User, \
    Registration, Major, StudentMajor, Instructor


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

        self.autumn = Term()
        self.autumn.quarter = Term.AUTUMN
        self.autumn.year = 2015
        self.autumn.save()

        self.summer = Term()
        self.summer.quarter = Term.SUMMER
        self.summer.year = 2015
        self.summer.save()

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

        self.autumn_ess = CourseOffering()
        self.autumn_ess.course = self.course
        self.autumn_ess.term = self.autumn
        self.autumn_ess.current_enrollment = 19
        self.autumn_ess.limit_estimate_enrollment = 25
        self.autumn_ess.save()

        self.ess_instructor_user = User()
        self.ess_instructor_user.uwnetid = "jinstructor"
        self.ess_instructor_user.save()

        self.ess_instructor = Instructor()
        self.ess_instructor.user = self.ess_instructor_user
        self.ess_instructor.course = self.course
        self.ess_instructor.term = self.spring
        self.ess_instructor.save()

        self.ess_instructor2 = Instructor()
        self.ess_instructor2.user = self.ess_instructor_user
        self.ess_instructor2.course = self.course
        self.ess_instructor2.term = self.winter
        self.ess_instructor2.save()

        self.ess_instructor3 = Instructor()
        self.ess_instructor3.user = self.ess_instructor_user
        self.ess_instructor3.course = self.course
        self.ess_instructor3.term = self.autumn
        self.ess_instructor3.save()

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

        for x in range(0, 10):
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
        reg.grade = 2.8
        reg.course = self.course
        reg.term = self.autumn
        reg.credits = 5
        reg.user = self.students[3]
        reg.save()
        self.registrations.append(reg)

        reg = Registration()
        reg.grade = 2.9
        reg.course = self.course
        reg.term = self.summer
        reg.credits = 5
        reg.user = self.students[3]
        reg.save()
        self.registrations.append(reg)

        reg = Registration()
        reg.grade = 0.0
        reg.course = self.cse_142
        reg.term = self.autumn
        reg.credits = 5
        reg.user = self.students[4]
        reg.save()
        self.registrations.append(reg)

        reg = Registration()
        reg.grade = 3.7
        reg.course = self.course
        reg.term = self.autumn
        reg.credits = 5
        reg.user = self.students[5]
        reg.save()
        self.registrations.append(reg)

        reg = Registration()
        reg.credits = 5
        reg.course = self.course
        reg.term = self.winter
        reg.user = self.students[5]
        reg.grade = 0.0
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
        reg.save()

        reg = Registration()
        reg.credits = 5
        reg.course = self.course
        reg.term = self.winter
        reg.user = self.students[7]
        reg.grade = ""
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
        self.assertEqual(len(concurrent), 2)
        self.assertEqual(concurrent[0]['number_students'], 4)

    def test_get_students(self):
        spring_students = self.spring_ess.get_students()
        self.assertEqual(len(spring_students), 3)

        winter_students = self.winter_ess.get_students()
        self.assertEqual(len(winter_students), 5)

    def test_majors(self):
        majors = self.winter_ess.get_majors()
        self.assertEqual(len(majors), 2)

    def test_graduated_majors(self):
        graduated_majors = self.winter_ess.get_graduated_majors()
        self.assertEqual(len(graduated_majors), 1)
        self.assertEqual(graduated_majors[0]['number_students'], 1)

    def test_student_cgpa(self):
        gpas = self.winter_ess.get_gpas()
        cgpa = self.winter_ess.get_cumulative_median_gpa(gpas)
        self.assertEqual(cgpa, 2.85)

    def test_historic_fail_rate(self):
        fail_rate = self.spring_ess.get_fail_rate()
        self.assertEqual(fail_rate, 1.0 / 10.0)

    def test_past_json(self):
        json = self.spring_ess.past_offerings_json_object()
        self.assertEqual(len(json['past_offerings']['terms']), 2)
        self.assertEqual(json['past_offerings']['enrollment'], 44)

    def test_get_grades(self):
        grades = self.winter_ess.get_grades()
        self.assertEqual(grades, [3.5, 3.5, 0.0, 2.4])

    def test_student_majors(self):
        majors = self.winter_ess.get_majors()

        self.assertEqual(len(majors), 2)

        self.assertEqual(majors[0]['major_name'], 'Computer Science')
        self.assertEqual(majors[0]['number_students'], 2)

        self.assertEqual(majors[1]['major_name'], 'Pre Science')
        self.assertEqual(majors[1]['number_students'], 2)

    def test_process_grade_totals(self):

        grade_totals = []

        grades = [2.0, 3.6, 0.0]

        grade_totals.append({
            'grade': grades[0],
            'credits': 5,
            'total': 2,
            'user': 0
        })

        grade_totals.append({
            'grade': grades[1],
            'credits': 5,
            'total': 3,
            'user': 0
        })

        grade_totals.append({
            'grade': grades[2],
            'credits': 5,
            'total': 1,
            'user': 0
        })

        grades = self.winter_ess._process_grade_totals(grade_totals)

        self.assertEqual(2.47, grades[0])

    def tearDown(self):
        for stumaj in self.student_majors:
            stumaj.delete()

        for reg in self.registrations:
            reg.delete()

        for student in self.students:
            student.delete()

        for major in self.majors:
            major.delete()

        self.ess_instructor.delete()
        self.ess_instructor2.delete()
        self.ess_instructor3.delete()
        self.ess_instructor_user.delete()

        self.spring_cse.delete()
        self.cse_142.delete()
        self.spring_ess.delete()
        self.winter_ess.delete()
        self.autumn_ess.delete()
        self.course.delete()
        self.spring.delete()
        self.winter.delete()
