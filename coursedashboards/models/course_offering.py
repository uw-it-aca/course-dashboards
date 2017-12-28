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
    def retrieve_course_info(self):
        """
        Retrieves all relevant Django models from the database
        :return:
        """
        threads = []
        targets = [self.retrieve_registrations, self.set_instructors]
        for target in targets:
            t = Thread(target=self.retrieve_registrations,
                       args=())
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    @profile
    def retrieve_registrations(self):
        # retrieve all registrations for this CourseOffering
        self.students = self.get_students()

        # retrieve all student Registrations for concurrent course and GPA
        self.student_registrations = self.get_all_student_registrations()
        repr(self.student_registrations)

    @profile
    def get_student_gpa(self, registrations):
        """
        Return current gpa for given student
        (assumption: all student registrations are modelled)
        """
        try:
            points = 0.0
            credits = 0
            for reg in registrations:
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

            user_registrations = {}
            for registration in self.get_all_student_registrations():
                id = registration.user_id

                if id not in user_registrations:
                    user_registrations[id] = []

                user_registrations[id].append(registration)

            for user in user_registrations:
                gpa = self.get_student_gpa(user_registrations[user])

                if gpa is not None:
                    cumulative.append(gpa)

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

    def set_instructors(self):
        self.instructors = self.get_instructors()

    @profile
    def get_instructors(self):
        if not hasattr(self, 'instructors'):
            self.instructors = [{
                'display_name': inst.user.display_name,
                'uwnetid': inst.user.uwnetid,
                'email': inst.user.email
            } for inst in Instructor.objects.filter(course=self.course,
                                                    term=self.term)]
        else:
            return self.instructors

    def get_all_student_registrations(self):
        """
        Returns all students' registrations
        :return:
        """
        students = self.get_students().values_list('user_id', flat=True)
        if not hasattr(self, 'student_registrations'):
            self.student_registrations = Registration.objects.filter(
                user_id__in=students).select_related('course', 'term')

        return self.student_registrations

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
        for reg in self.get_all_student_registrations():
            if reg.course.id != self.course.id and reg.term == self.term:
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
        # TODO: use Aggregator API here
        return [sm.major.major for sm in StudentMajor.objects.filter(
            user_id__in=students.values_list('user_id', flat=True),
            term=self.term).select_related('major')]

    @profile
    def last_student_undergraduate_major(self, students):

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
            majors = sorted(majors, cmp=StudentMajor.sort_by_term,
                            reverse=True)

            graduated_term = majors[0].term

            majors = [major for major in majors
                      if major.term == graduated_term]

            major_list += [sm.major.major for sm in majors]

        return major_list

    @profile
    def get_graduated_majors(self):
        return self._get_majors(self.last_student_undergraduate_major)

    @profile
    def get_majors(self):
        return self._get_majors(self.student_majors_for_term)

    def _get_majors(self, student_majors):
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

    def get_fail_rate(self):
        # TODO: use Aggregator API here
        past_objs = []
        threads = []

        for co in CourseOffering.objects.filter(
                course=self.course).select_related('course', 'term'):
            past_obj = {}
            past_objs.append(past_obj)

            t = Thread(target=co.set_past_course_grades,
                       args=(past_obj,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total = 0.0
        failed = 0.0
        for past_obj in past_objs:
            total += len(past_obj['course_grades'])
            failed += len([grade for grade in past_obj['course_grades']
                          if grade < 0.7])

        if total == 0:
            return 0

        return failed / total

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

    def set_fail_rate(self, json_obj):
        json_obj['failure_rate'] = self.get_fail_rate()

    def set_json_cumulative_median(self, json_obj):
        json_obj['current_median'] = self.get_cumulative_median_gpa()

    def set_json_concurrent_courses(self, json_obj):
        json_obj['concurrent_courses'] = self.concurrent_courses()

    def set_json_current_student_majors(self, json_obj):
        json_obj['current_student_majors'] = self.get_majors()

    def set_course_data(self, json_obj):

        # retrieve info used by multiple threads
        self.retrieve_course_info()

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

        log_profile_data('%s,%s' % (self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    def base_json_object(self):
        json_obj = {
            'curriculum': self.course.curriculum,
            'course_number': self.course.course_number,
            'section_id': self.course.section_id,
            'course_title': self.course.course_title,
            'section_label': '%s' % self,
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

    def set_past_offering_data(self, past_obj):

        # retrieve info used by multiple threads
        self.retrieve_course_info()

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
        quarters = 40

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
