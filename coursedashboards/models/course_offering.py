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

    def get_students(self):
        """
        Return Registration queryset for this course offering
        """
        if not hasattr(self, 'students'):
            self.students = Registration.objects.filter(
                course=self.course, term=self.term)

        return self.students

    def get_median_gpa(self):
        """
        Calculates median grade point average for course offering
        """
        grades = [float(s.grade) for s in self.get_students()
                  if re.match(r'^[0-4]\.\d+$', s.grade)]
        return statistics.median(grades) if len(grades) else None

    def get_repeating_total(self):
        """
        Number of students repeating this course offering
        """
        return len(self.get_students().filter(is_repeat=True))

    def get_past_offerings(self):
        """
        List of past course offerings
        """
        min_offerings = 1
        quarters = 20

        offerings = [{
            "year": co.term.year,
            "quarter": co.term.quarter,
            "instructors": co.get_instructors(),
            "majors": co.get_majors(),
            "concurrent_courses": self.concurrent_courses(),
            "latest_majors": self.get_recent_majors()
        } for co in CourseOffering.objects.filter(
            course=self.course).select_related('course', 'term')
                     if co.id != self.id][:quarters]

        return offerings if len(offerings) >= min_offerings else []

    def get_instructors(self):
        return [{
            'display_name': inst.user.display_name,
            'uwnetid': inst.user.uwnetid,
            'email': inst.user.email
        } for inst in Instructor.objects.filter(course=self.course,
                                                term=self.term)]

    def all_student_registrations(self):
        """
        Return given user's Courses for this term
        """
        students = list(self.get_students().values_list('user_id', flat=True))
        return Registration.objects.filter(
            user_id__in=students, term=self.term).select_related('course')

    def concurrent_courses(self):
        course_dict = {}
        for reg in self.all_student_registrations():
            if reg.course.id != self.course.id:
                name = "%s" % reg.course
                if name in course_dict:
                    course_dict[name] += 1
                else:
                    course_dict[name] = 1

        total_students = float(len(self.get_students()))
        return [{
            "course": sort,
            "number_students": course_dict[sort],
            "percent_students": round(
                (float(course_dict[sort]) / total_students) * 100.0, 2)
        } for sort in sorted(course_dict, reverse=True, key=course_dict.get)]

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
        total_students = 0.0
        for student in self.get_students():
            total_students += 1
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
                "percent_students": round(
                    (float(majors_dict[sort]) / total_students) * 100.0, 2)
            })

        return top_majors

    def json_object(self):
        return {
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'current_enrollment': self.current_enrollment,
            'limit_estimate_enrollment': self.limit_estimate_enrollment,
            'current_repeating': self.get_repeating_total(),
            'current_median': self.get_median_gpa(),
            'concurrent_courses': self.concurrent_courses(),
            'current_student_majors': self.get_majors(),
            'past_offerings': self.get_past_offerings(),
        }

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')
        ordering = ['-term__year', '-term__quarter']

    def __str__(self):
        return "%s,%s" % (self.term, self.course)
