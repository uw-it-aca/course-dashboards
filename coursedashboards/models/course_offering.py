import statistics
import re
from django.db import models
from coursedashboards.models.instructor import Instructor
from coursedashboards.models.course import Course
from coursedashboards.models.term import Term
from coursedashboards.models.registration import Registration
from coursedashboards.models.major import StudentMajor
import logging


logger = logging.getLogger(__name__)


class CourseOffering(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT)
    current_enrollment = models.PositiveSmallIntegerField()
    limit_estimate_enrollment = models.PositiveSmallIntegerField()
    canvas_course_url = models.CharField(max_length=2000)
    # num_repeating = models.IntegerField()
    # median_gpa = models.FloatField()

    def get_median_gpa(self):
        """
        Calculates median grade point average for course offering
        """
        students, total = self.get_students()
        grades = []
        for student in students:
            if re.match(r'^[0-4]\.\d+$', student.grade):
                grades.append(float(student.grade))

        return statistics.median(grades) if len(grades) else None

    def get_repeating_total(self):
        students, total = self.get_students()
        return len(students.filter(is_repeat=True))

    def get_past_offerings(self):
        years = 5
        min_offerings = 2
        # get past offerings of course up to x years ago,
        # need to find at least min_offerings in order to display data

        start_quarter = next((i for i, v in enumerate(Term.QUARTERNAME_CHOICES)
                              if v[0] == self.term.quarter))
        test_quarter = start_quarter + 1 if (start_quarter < 4) else 0
        test_year = self.term.year - years if (
            test_quarter > 0) else self.term.year - (years-1)

        # look for past offerings in each quarter
        # create object containing section term info plus every student grade

        past_offerings = []

        while test_year <= self.term.year:
            test_quarter_name = Term.QUARTERNAME_CHOICES[test_quarter][0]
            try:
                term = Term.objects.get(
                    year=test_year, quarter=test_quarter_name)

                section = CourseOffering.objects.get(
                    course=self.course, term=term)

                past_offerings.append({
                    "year": test_year,
                    "quarter": test_quarter_name,
                    "instructors": section.get_instructors(),
                    "majors": section.get_majors(),
                    "concurrent_courses": self.concurrent_courses(),
                    "latest_majors": self.get_recent_majors()
                })
            except Term.DoesNotExist:
                logger.error('No Data For term: %s,%s' % (
                    test_year, test_quarter_name))
            except CourseOffering.DoesNotExist:
                pass

            if test_quarter == 3:
                test_year += 1
                test_quarter = 0
            else:
                test_quarter += 1

            if (test_year == self.term.year and
                    test_quarter == start_quarter):
                break

        return past_offerings if len(past_offerings) >= min_offerings else []

    def get_instructors(self):
        """
        Return Instructor queryset for this course offering
        """
        instructor_list = []
        instructors = Instructor.objects.filter(
            course=self.course, term=self.term)
        for instructor in instructors:
            instructor_list.append({
                'display_name': instructor.user.display_name,
                'uwnetid': instructor.user.uwnetid,
                'email': instructor.user.email
            })

        return instructor_list

    def get_students(self):
        """
        Return Registration queryset for this course offering
        """
        if not hasattr(self, 'students'):
            self.students = Registration.objects.filter(
                course=self.course, term=self.term)
            self.student_count = len(self.students)

        return (self.students, self.student_count)

    def courses_for_student(self, student):
        """
        Return given user's Courses for this term
        """
        return Registration.objects.filter(
            user=student.user, term=self.term).values_list(
                'course_id', flat=True)

    def concurrent_courses(self):
        course_dict = {}
        students, total_students = self.get_students()
        for student in students:
            for course_id in self.courses_for_student(student):
                if course_id != self.course.id:
                    course_name = "%s" % Course.objects.get(id=course_id)
                    if course_name in course_dict:
                        course_dict[course_name] += 1
                    else:
                        course_dict[course_name] = 1

        sorted_courses = sorted(course_dict, reverse=True, key=course_dict.get)
        top_courses = []
        for sort in sorted_courses:
            top_courses.append({
                "course": sort,
                "number_students": course_dict[sort],
                "percent_students": round(
                    (float(course_dict[sort]) / float(total_students)) *
                    100.0, 2)
            })

        return top_courses

    def student_majors_for_term(self, student):
        return StudentMajor.objects.filter(
            user=student.user, term=self.term)

    def last_student_major(self, student):
        return StudentMajor.objects.filter(
            user=student.user, term=student.user.last_enrolled)

    def get_recent_majors(self):
        return self._get_majors(self.last_student_major)

    def get_majors(self):
        return self._get_majors(self.student_majors_for_term)

    def _get_majors(self, student_majors):
        majors_dict = {}
        students, total_students = self.get_students()
        for student in students:
            majors = student_majors(student)
            for major in majors:
                if major.major.major in majors_dict:
                    majors_dict[major.major.major] += 1
                else:
                    majors_dict[major.major.major] = 1

        top_majors = []
        sorted_majors = sorted(majors_dict, reverse=True, key=majors_dict.get)
        for sort in sorted_majors:
            top_majors.append({
                "major": sort,
                "number_students": majors_dict[sort],
                "percent_students":
                round(
                    (float(majors_dict[sort]) / float(total_students)) *
                    100.0, 2)
            })

        return top_majors

    def json_object(self):
        return {
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'current_enrollment': self.current_enrollment,
            'limit_estimate_enrollment': self.limit_estimate_enrollment,
            'num_repeating': self.get_repeating_total(),
            'current_median': self.get_median_gpa(),
            'concurrent_courses': self.concurrent_courses(),
            'current_student_majors': self.get_majors(),
            'past_offerings': self.get_past_offerings(),
        }

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')

    def __str__(self):
        return "%s,%s" % (self.term, self.course)
