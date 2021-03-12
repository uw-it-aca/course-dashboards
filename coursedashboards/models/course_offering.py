from django.conf import settings
from django.db.models import Count
from statistics import median
from statistics import StatisticsError
from collections import defaultdict
from django.db import models
from coursedashboards.models.instructor import Instructor
from coursedashboards.models.course import Course
from coursedashboards.models.course_grade_average import CourseGradeAverage
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
    def get_registrations(self):
        """
        Return Registration queryset for this course offering
        """
        return Registration.objects.filter(course=self.course, term=self.term)

    @profile
    def get_students(self):
        return list(self.get_registrations().values_list('user_id', flat=True))

    @profile
    def get_student_count(self):
        return float(self.get_registrations().count())

    @profile
    def get_gpas(self):
        registrations = Registration.objects.filter(
            user_id__in=self.get_students()) \
            .filter(term__term_key__lt=self.term.term_key) \
            .values('grade', 'credits', 'user') \
            .annotate(total=Count('grade'))

        cumulative = self._process_grade_totals(registrations)

        return cumulative

    @profile
    def get_cumulative_median_gpa(self, gpas):
        """
        Return median gpa for this course offering at the time it was offered
        """
        try:
            return round(median(gpas), 2)
        except StatisticsError:
            return None

    def _process_grade_totals(self, registrations):
        user_grades = {}

        for registration in registrations:
            userid = registration['user']

            if userid not in user_grades:
                user_grades[userid] = {
                    'credits': 0,
                    'grade_points': 0
                }

            self._add_grade_entry(user_grades[userid], registration)

        grades = []

        for userid in user_grades:
            credits = user_grades[userid]['credits']
            grade_points = user_grades[userid]['grade_points']

            if credits != 0:
                grades.append(grade_points / credits)

        return grades

    @staticmethod
    def _add_grade_entry(user_grade, grade_entry):
        try:
            credits = float(grade_entry['credits'])
            grade = float(grade_entry['grade'])
            total = grade_entry['total']

            user_grade['credits'] += credits * total
            user_grade['grade_points'] += grade * total * credits
        except ValueError:
            pass

    @profile
    def get_grades(self):
        """
        Return grade array for course offering
        """
        return [float(grade) for grade in Registration.objects.filter(
            course=self.course, term=self.term).values_list('grade', flat=True)
                if grade is not None and grade[0] in '01234']

    @profile
    def get_repeating_total(self):
        """
        Number of students repeating this course offering
        """
        return self.get_registrations().filter(is_repeat=True).count()

    @profile
    def get_instructors(self):
        return [{
            'uwnetid': inst.user.uwnetid,
            'display_name': inst.user.display_name,
            'preferred_first_name': inst.user.preferred_first_name,
            'preferred_middle_name': inst.user.preferred_middle_name,
            'preferred_surname': inst.user.preferred_surname,
            'email': inst.user.email,
            'is_student': inst.user.is_student,
            'is_staff': inst.user.is_staff,
            'is_employee': inst.user.is_employee,
            'is_alum': inst.user.is_alum,
            'is_faculty': inst.user.is_faculty
        } for inst in Instructor.objects.filter(course=self.course,
                                                term=self.term)]

    @profile
    def all_student_registrations(self):
        """
        Return given user's Courses for this term
        """
        return Registration.objects.filter(
            user_id__in=self.get_students(),
            term=self.term).select_related('course')

    @profile
    def concurrent_courses(self):
        course_dict = {}
        for reg in self.all_student_registrations():
            if reg.course.id != self.course.id:
                try:
                    cga = CourseGradeAverage.objects.get(
                        curriculum=reg.course.curriculum,
                        course_number=reg.course.course_number)
                    mean_gpa = cga.grade
                except CourseGradeAverage.DoesNotExist:
                    mean_gpa = ''

                name = "{}-{}|{}|{}".format(reg.course.curriculum,
                                            reg.course.course_number,
                                            reg.course.course_title,
                                            mean_gpa)
                if name in course_dict:
                    course_dict[name] += 1
                else:
                    course_dict[name] = 1

        total_students = self.get_student_count()
        return [{
            "course": sort.split("|")[0],
            "title": sort.split("|")[1],
            "number_students": course_dict[sort],
            "percent_students": round(
                (float(course_dict[sort]) / total_students) * 100.0, 2),
            "mean_gpa": sort.split("|")[2]
        } for sort in sorted(course_dict, reverse=True, key=course_dict.get)]

    @profile
    def student_majors_for_term(self):
        return [sm.major.major for sm in StudentMajor.objects.filter(
            user_id__in=self.get_students(),
            term=self.term).select_related('major')]

    @profile
    def last_student_undergraduate_major(self):
        students = self.get_registrations().select_related('user')
        class_majors = self.retrieve_course_majors(students)
        student_majors = self.sort_major_by_user(class_majors)
        return self.process_individual_majors(student_majors)

    @profile
    def sort_major_by_user(self, class_majors):
        student_majors = {}

        for major in class_majors:
            if major.user_id not in student_majors:
                majors = []
                student_majors[major.user_id] = majors
            else:
                majors = student_majors[major.user_id]

            majors.append(major)

        return student_majors

    @profile
    def retrieve_course_majors(self, students):
        users = [student.user for student in students if student.user.is_alum]

        queryset = StudentMajor.objects.filter(user__in=users,
                                               major__degree_level=1) \
            .select_related('major', 'term')
        # trigger query for profiling:
        repr(queryset)

        return queryset

    @profile
    def process_individual_majors(self, student_majors):
        major_list = []
        for student in student_majors:

            majors = student_majors[student]
            majors = sorted(majors, reverse=True)

            graduated_term = majors[0].term

            majors = [major for major in majors
                      if major.term == graduated_term]

            major_list += [sm.major.major for sm in majors]

        return major_list

    @profile
    def get_graduated_majors(self):
        return self._get_majors(self.last_student_undergraduate_major())

    @profile
    def get_majors(self):
        return self._get_majors(self.student_majors_for_term())

    def _get_majors(self, majors):
        total_students = self.get_student_count()
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

    @profile
    def get_fail_rate(self):

        registrations = Registration.objects.filter(course=self.course)\
            .values('grade').annotate(total=Count('grade'))

        total = 0.0
        failed = 0.0

        for reg in registrations:
            if len(reg['grade']) > 0 and reg['grade'][0] in '01234':
                if float(reg['grade']) == 0.0:
                    failed += reg['total']

                total += reg['total']

        if total == 0:
            return 0

        return failed / total

    def brief_json_object(self):
        json_obj = {
            'section_label': '{}'.format(self),
            'year': self.term.year,
            'quarter': self.term.quarter,
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'course_title': self.course.course_title
        }

        return json_obj

    def set_json_repeating_total(self, json_obj):
        json_obj['current_repeating'] = self.get_repeating_total()

    def set_fail_rate(self, json_obj):
        json_obj['failure_rate'] = self.get_fail_rate()

    def set_json_cumulative_median(self, json_obj):
        gpas = self.get_gpas()
        json_obj['gpas'] = gpas
        json_obj['current_median'] = self.get_cumulative_median_gpa(gpas)

    def set_json_course_grades(self, json_obj):
        grades = self.get_grades()
        json_obj['course_grades'] = grades
        json_obj['median_course_grade'] = self.get_cumulative_median_gpa(
            grades)

    def set_json_concurrent_courses(self, json_obj):
        json_obj['concurrent_courses'] = self.concurrent_courses()

    def set_json_current_student_majors(self, json_obj):
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

        t = Thread(target=self.set_json_course_grades,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_json_concurrent_courses,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_json_current_student_majors,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        for t in threads:
            t.join()

    @profile
    def json_object(self):
        json_obj = self.base_json_object()

        json_obj['display_course'] = True

        self.set_course_data(json_obj)

        fields = ["current_repeating", "current_student_majors",
                  "current_student_majors", "concurrent_courses"]

        for field in fields:
            if field not in json_obj:
                raise Exception("There was an error in data processing!")

        log_profile_data('{},{}'.format(self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    def base_json_object(self):
        json_obj = {
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'year': self.term.year,
            'quarter': self.term.quarter,
            'course_title': self.course.course_title,
            'section_label': '{}'.format(self),
            'current_enrollment': self.current_enrollment,
            'limit_estimate_enrollment': self.limit_estimate_enrollment,
            'canvas_course_url': self.canvas_course_url,
            'display_course': False
        }

        return json_obj

    def set_past_offering_instructors(self, past_obj):
        past_obj['instructors'] = self.get_instructors()

    def set_past_offering_majors(self, past_obj):
        past_obj['majors'] = self.get_majors()

    def set_past_concurrent_courses(self, past_obj):
        past_obj['concurrent_courses'] = self.concurrent_courses()

    def set_past_latest_majors(self, past_obj):
        past_obj['latest_majors'] = self.get_graduated_majors()

    def set_past_course_grades(self, past_obj):
        past_obj['course_grades'] = self.get_grades()

    def set_past_median_gpa(self, past_obj):
        past_obj['gpas'] = self.get_gpas()

    def set_past_offering_data(self, past_obj):
        threads = []
        t = Thread(target=self.set_past_offering_instructors,
                   args=(past_obj,))
        threads.append(t)
        t.start()

        if getattr(settings, "HISTORIC_CGPA_ENABLED", True):
            t = Thread(target=self.set_past_median_gpa,
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
            "enrollment": course_offering.current_enrollment
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

        fields = ["instructors", "majors", "concurrent_courses",
                  "course_grades", "latest_majors"]

        for offering in offerings:
            for field in fields:
                if field not in offering:
                    raise Exception("There was an error in data processing!")

        return offerings if len(offerings) >= min_offerings else []

    def past_offerings_json_object(self):
        json_obj = {
            'past_offerings': self.get_past_offerings(),
        }

        log_profile_data(
            '{},{}: PAST: '.format(self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')
        ordering = ['-term__year', '-term__quarter']

    def __str__(self):
        return "{}-{}".format(self.term, self.course)
