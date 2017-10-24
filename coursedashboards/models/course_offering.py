from statistics import median
from statistics import StatisticsError
from collections import defaultdict
from django.db import models
from coursedashboards.models.instructor import Instructor
from coursedashboards.models.course import Course
from coursedashboards.models.term import Term
from coursedashboards.models.registration import Registration
from coursedashboards.models.major import StudentMajor
from coursedashboards.util.profile import (
    profile, log_profile_data, clear_prof_data)
from threading import Thread
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

    @profile
    def get_students(self):
        """
        Return Registration queryset for this course offering
        """
        if not hasattr(self, 'students'):
            self.students = Registration.objects.filter(
                course=self.course, term=self.term)

        return self.students

    @profile
    def get_student_gpa(self, student):
        """
        Return current gpa for given student
        (assumption: all student registrations are modelled)
        """
        try:
            points = 0.0
            credits = 0
            for reg in Registration.objects.filter(user=student.user):
                try:
                    course_credits = int(reg.credits)
                    points += (float(reg.grade) * course_credits)
                    credits += course_credits
                except ValueError:
                    pass

            return round(points / credits, 2)
        except ZeroDivisionError:
            return None

    def set_student_gpa(self, student, cumulative):
        gpa = self.get_student_gpa(student)
        if gpa:
            cumulative.append(gpa)

    @profile
    def get_cumulative_median_gpa(self):
        """
        Return median gpa for this course offering
        """
        try:
            cumulative = []
            threads = []
            for student in self.get_students():
                t = Thread(target=self.set_student_gpa,
                           args=(student, cumulative,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            return round(median(cumulative), 2)
        except StatisticsError:
            return None

    @profile
    def get_grades(self):
        """
        Return grade array for course offering
        """
        return [float(s.grade) for s in self.get_students()
                if s.grade[0] in '01234']

    @profile
    def get_repeating_total(self):
        """
        Number of students repeating this course offering
        """
        return len(self.get_students().filter(is_repeat=True))

    @profile
    def get_instructors(self):
        return [{
            'display_name': inst.user.display_name,
            'uwnetid': inst.user.uwnetid,
            'email': inst.user.email
        } for inst in Instructor.objects.filter(course=self.course,
                                                term=self.term)]

    @profile
    def all_student_registrations(self):
        """
        Return given user's Courses for this term
        """
        students = list(self.get_students().values_list('user_id', flat=True))
        return Registration.objects.filter(
            user_id__in=students, term=self.term).select_related('course')

    @profile
    def concurrent_courses(self):
        course_dict = {}
        for reg in self.all_student_registrations():
            if reg.course.id != self.course.id:
                name = "%s" % reg.course
                name = name[:name.rindex('-')]
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

    @profile
    def student_majors_for_term(self, students):
        return [sm.major.major for sm in StudentMajor.objects.filter(
            user_id__in=students.values_list('user_id', flat=True),
            term=self.term).select_related('major')]

    @profile
    def last_student_major(self, students):
        major_list = []
        for student in students:
            majors = StudentMajor.objects.filter(
                user=student.user,
                term=student.user.last_enrolled,
                degree_level=1).select_related('major')
            major_list += [sm.major.major for sm in majors]

        return major_list

    @profile
    def get_recent_majors(self):
        return self._get_majors(self.last_student_major)

    @profile
    def get_majors(self):
        return self._get_majors(self.student_majors_for_term)

    def _get_majors(self, student_majors):
        majors_dict = {}
        students = self.get_students().select_related('user')
        total_students = float(len(students))
        majors = student_majors(students)
        majors_dict = defaultdict(int)
        for major in majors:
            majors_dict[major] += 1

        return [{
            "major": sort,
            "number_students": majors_dict[sort],
            "percent_students": round(
                (float(majors_dict[sort]) / total_students) * 100.0, 2)
            } for sort in sorted(
                majors_dict, reverse=True, key=majors_dict.get)]

    def brief_json_object(self):
        json_obj = {
            'section_label': '%s' % self,
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id
        }

        return json_obj

    def set_json_repeating_total(self, json_obj):
        json_obj['current_repeating'] = self.get_repeating_total()

    def set_json_cumulative_median(self, json_obj):
        json_obj['current_median'] = self.get_cumulative_median_gpa()

    def set_json_concurrent_courses(self, json_obj):
        json_obj['concurrent_courses'] = self.concurrent_courses()

    def set_json_curren_student_majors(self, json_obj):
        json_obj['current_student_majors'] = self.get_majors()

    def set_course_data(self, json_obj):
        threads = []
        t = Thread(target=self.set_json_repeating_total,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_json_cumulative_median,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_json_concurrent_courses,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_json_curren_student_majors,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        for t in threads:
            t.join()

    @profile
    def json_object(self):
        json_obj = {
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'course_title': self.course.course_title,
            'section_label': '%s' % self,
            'current_enrollment': self.current_enrollment,
            'limit_estimate_enrollment': self.limit_estimate_enrollment,
            'canvas_course_url': self.canvas_course_url,
        }

        self.set_course_data(json_obj)

        log_profile_data('%s,%s' % (self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    def set_past_offering_instructors(self, past_obj):
        past_obj['instructors'] = self.get_instructors()

    def set_past_offering_majors(self, past_obj):
        past_obj['majors'] = self.get_majors()

    def set_past_concurrent_courses(self, past_obj):
        past_obj['concurrent_courses'] = self.concurrent_courses()

    def set_past_latest_majors(self, past_obj):
        past_obj['latest_majors'] = self.get_recent_majors()

    def set_past_course_grades(self, past_obj):
        past_obj['course_grades'] = self.get_grades()

    def set_past_offering_data(self, past_obj):
        threads = []
        t = Thread(target=self.set_past_offering_instructors,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_offering_majors,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_concurrent_courses,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_latest_majors,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_course_grades,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        for t in threads:
            t.join()

    def set_past_offering(self, course_offering, offerings):
        off_obj = {
            "year": course_offering.term.year,
            "quarter": course_offering.term.quarter,
        }

        course_offering.set_past_offering_data(off_obj)
        offerings.append(off_obj)

    @profile
    def get_past_offerings(self):
        """
        List of past course offerings
        """
        min_offerings = 1
        quarters = 20

        threads = []
        offerings = []
        for co in CourseOffering.objects.filter(
                course=self.course).select_related('course', 'term'):
            if co.id != self.id:
                t = Thread(target=self.set_past_offering,
                           args=(co, offerings,))
                threads.append(t)
                t.start()

                if len(threads) >= quarters:
                    break

        for t in threads:
            t.join()

        return offerings if len(offerings) >= min_offerings else []

    def past_offerings_json_object(self):
        json_obj = {
            'past_offerings': self.get_past_offerings(),
        }

        log_profile_data('%s,%s: PAST: ' % (self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')
        ordering = ['-term__year', '-term__quarter']

    def __str__(self):
        return "%s-%s" % (self.term, self.course)
