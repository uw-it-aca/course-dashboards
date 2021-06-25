from django.conf import settings
from django.db.models import Count, Sum
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
    def get_registrations(self, terms=None):
        """
        Return Registration queryset for this course offering
        """
        filter_parms = self._filter_parms(terms)

        if settings.DEBUG:
            try:
                if not self._get_reg_explained:
                    pass
            except AttributeError:
                self._get_reg_explained = True
                self._explain(
                    "registrations", Registration.objects.filter(
                        filter_parms
                    ).explain())

        return Registration.objects.filter(filter_parms)

    @profile
    def _filter_parms(self, terms=None):
        if terms:
            term_filter = models.Q(term__in=terms)
        else:
            term_filter = models.Q(term=self.term)

        return term_filter & models.Q(course=self.course)

    @profile
    def get_students(self, terms=None):
        if settings.DEBUG:
            self._explain("students", self.get_registrations(
                terms=terms
            ).values_list(
                'user_id', flat=True
            ).explain())

        return self.get_registrations(
            terms
        ).values_list(
            'user_id', flat=True
        )

    @profile
    def get_student_count(self, terms=None):
        return float(self.get_registrations(terms=terms).count())

    @profile
    def get_gpas(self, terms=None):
        if settings.DEBUG:
            self._explain("get_gpas", Registration.objects.filter(
                user_id__in=self.get_students(terms=terms),
                term__term_key__lt=self.term.term_key
            ).values(
                'grade', 'credits', 'user'
            ).annotate(
                total=Count('grade')
            ).explain())

        registrations = Registration.objects.filter(
            user_id__in=self.get_students(terms=terms),
            term__term_key__lt=self.term.term_key
        ).values(
            'grade', 'credits', 'user'
        ).annotate(
            total=Count('grade')
        )

        return self._process_grade_totals(registrations)

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
                grades.append(round(grade_points / credits, 2))

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
    def get_grades(self, terms=None):
        """
        Return grade array for course offering
        """
        return [float(grade) for grade in list(
            self.get_registrations(
                terms=terms
            ).values_list(
                'grade', flat=True
            ))
                if self._is_grade_value(grade)]

    @profile
    def get_repeating_total(self, terms=None):
        """
        Number of students repeating this course offering
        """
        return self.get_registrations(
            terms=terms
        ).filter(
            is_repeat=True
        ).count()

    @profile
    def get_instructors(self, terms=None):
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
        } for inst in Instructor.objects.filter(self._filter_parms(terms))]

    @profile
    def get_enrollment_count(self, terms=None):
        filter_parms = self._filter_parms(terms)

        return CourseOffering.objects.filter(
            filter_parms
        ).aggregate(
            Sum('current_enrollment')
        )['current_enrollment__sum']

    def _course_id(self, course):
        return "{}-{}".format(course.curriculum, course.course_number)

    @profile
    def concurrent_courses(self, terms=None):
        concurrent = {}
        courses = {}
        students = set()

        if terms:
            filter_parms = models.Q(term__in=terms)
        else:
            filter_parms = models.Q(term=self.term)

        filter_parms &= models.Q(user_id__in=self.get_students(terms))

        if settings.DEBUG:
            self._explain(
                "all student registrations",
                Registration.objects.filter(
                    filter_parms
                ).select_related(
                    'course'
                ).explain())

        all_students = Registration.objects.filter(
            filter_parms
        ).select_related(
            'course'
        )

        for reg in all_students:
            students.add(reg.user_id)
            if reg.course_id != self.course_id:
                course_id = self._course_id(reg.course)
                if course_id not in concurrent:
                    concurrent[course_id] = {
                        'course': course_id,
                        'title': reg.course.course_title,
                        'mean_gpa': '',
                        'students': 0
                    }

                concurrent[course_id]['students'] += 1

                if reg.course.curriculum not in courses:
                    courses[reg.course.curriculum] = set()

                courses[reg.course.curriculum].add(reg.course.course_number)

        query = models.Q()
        for curriculum, course_numbers in courses.items():
            query |= models.Q(curriculum=curriculum,
                              course_number__in=list(course_numbers))

        if settings.DEBUG:
            self._explain(
                "course grade avg",
                CourseGradeAverage.objects.filter(query).explain())

        for cga in CourseGradeAverage.objects.filter(query):
            try:
                concurrent[self._course_id(cga)]['mean_gpa'] = cga.grade
            except KeyError as ex:
                logger.error("Unexpected CourseGradeAverage: {}".format(ex))

        total_students = len(students)

        return [{
            "course": sort['course'],
            "title": sort['title'],
            "number_students": sort['students'],
            "percent_students": round(
                (float(sort['students']) / total_students) * 100.0, 2),
            "mean_gpa": sort['mean_gpa']
        } for sort in sorted(list(concurrent.values()),
                             key=lambda i: (i['students'], i['course']),
                             reverse=True)]

    @profile
    def student_majors_for_term(self, terms=None):
        if terms:
            filter_parms = models.Q(term__in=terms)
        else:
            filter_parms = models.Q(term=self.term)

        filter_parms &= models.Q(user_id__in=self.get_students(terms))

        if settings.DEBUG:
            self._explain("student majors", StudentMajor.objects.filter(
                filter_parms
            ).select_related(
                'major'
            ).explain())

        return [sm.major.major for sm in StudentMajor.objects.filter(
            filter_parms
        ).select_related(
            'major'
        )]

    @profile
    def last_student_undergraduate_major(self, terms=None):
        students = self.get_registrations(terms).select_related('user')
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

        queryset = StudentMajor.objects.filter(user_id__in=users,
                                               major__degree_level=1) \
            .select_related('major', 'term')

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
    def get_graduated_majors(self, terms=None):
        return self._get_majors(
            self.last_student_undergraduate_major(terms))

    @profile
    def get_majors(self, terms=None):
        return self._get_majors(self.student_majors_for_term(terms))

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
        total = 0.0
        failed = 0.0

        registrations = Registration.objects.filter(
            course=self.course
        ).values(
            'grade'
        ).annotate(
            total=Count('grade')
        )

        for reg in registrations:
            if self._is_grade_value(reg['grade']):
                if float(reg['grade']) == 0.0:
                    failed += reg['total']

                total += reg['total']

        return (failed / total) if total > 0 else 0

    @staticmethod
    def _is_grade_value(grade):
        return grade is not None and grade[:1].isdigit()

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

    @profile
    def set_past_offering_enrollment_count(self, past_obj, terms=None):
        past_obj['enrollment'] = self.get_enrollment_count(terms)

    @profile
    def set_past_offering_instructors(self, past_obj, terms=None):
        past_obj['instructors'] = self.get_instructors(terms)

    @profile
    def set_past_offering_majors(self, past_obj, terms=None):
        past_obj['majors'] = self.get_majors(terms)

    @profile
    def set_past_concurrent_courses(self, past_obj, terms=None):
        past_obj['concurrent_courses'] = self.concurrent_courses(terms)

    @profile
    def set_past_latest_majors(self, past_obj, terms=None):
        past_obj['latest_majors'] = self.get_graduated_majors(terms)

    @profile
    def set_past_course_grades(self, past_obj, terms=None):
        past_obj['course_grades'] = self.get_grades(terms)

    @profile
    def set_past_median_gpa(self, past_obj, terms=None):
        past_obj['gpas'] = self.get_gpas(terms)

    @profile
    def set_past_offering_data(self, past_obj, terms):
        threads = []

        t = Thread(target=self.set_past_offering_enrollment_count,
                   args=(past_obj, terms,))
        threads.append(t)
        t.start()

        if bool(getattr(settings, "HISTORIC_CGPA_ENABLED", True)):
            t = Thread(target=self.set_past_median_gpa,
                       args=(past_obj, terms,))
            threads.append(t)
            t.start()

        t = Thread(target=self.set_past_offering_majors,
                   args=(past_obj, terms,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_concurrent_courses,
                   args=(past_obj, terms,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_latest_majors,
                   args=(past_obj, terms,))
        threads.append(t)
        t.start()

        t = Thread(target=self.set_past_course_grades,
                   args=(past_obj, terms,))
        threads.append(t)
        t.start()

        for t in threads:
            t.join()

    @profile
    def get_past_sections(self):
        """
        List of past course sections
        """
        filter_parms = {
            'course': self.course
        }

        if settings.DEBUG:
            self._explain("get_past_sections",
                          Instructor.objects.filter(
                              **filter_parms
                          ).select_related(
                              'term', 'user'
                          ).explain())

        instructors = Instructor.objects.filter(
            **filter_parms
        ).select_related(
            'term', 'user'
        )

        sections = {}
        for i in instructors:
            if i.term.year not in sections:
                sections[i.term.year] = {}

            if i.term.quarter not in sections[i.term.year]:
                sections[i.term.year][i.term.quarter] = []

            sections[i.term.year][i.term.quarter].append({
                'uwnetid': i.user.uwnetid,
                'display_name': i.user.display_name,
                'preferred_first_name': i.user.preferred_first_name,
                'preferred_middle_name': i.user.preferred_middle_name,
                'preferred_surname': i.user.preferred_surname,
                'email': i.user.email,
                'is_student': i.user.is_student,
                'is_staff': i.user.is_staff,
                'is_employee': i.user.is_employee,
                'is_alum': i.user.is_alum,
                'is_faculty': i.user.is_faculty
            })

        return sections

    @profile
    def get_past_offerings(self, terms):
        """
        List of past course offerings
        """
        offerings = {
            'terms': ["{}".format(Term.objects.get(id=t)) for t in terms]
        }

        self.set_past_offering_data(offerings, terms)

        return offerings

    def past_offerings_json_object(
            self, past_year='', past_quarter='', instructor=None):

        # build filter for past offerings
        filter_parms = models.Q(course=self.course)

        try:
            filter_parms &= models.Q(term__year=int(past_year))
        except ValueError:
            pass

        try:
            quarter = past_quarter.lower()
            if quarter in ['winter', 'spring', 'summer', 'autumn']:
                filter_parms &= models.Q(term__quarter=quarter)
        except Exception:
            pass

        if instructor is not None:
            filter_parms &= models.Q(user__uwnetid=instructor)

        terms = Instructor.objects.filter(
            filter_parms
        ).exclude(
            term=self.term
        ).values_list(
            'term', flat=True
        )

        json_obj = {
            'past_offerings': self.get_past_offerings(terms),
            'sections': self.get_past_sections(),
            'filter': {
                'year': past_year,
                'quarter': past_quarter,
                'only_instructed': instructor is not None
            }
        }

        log_profile_data(
            '{},{}: PAST: '.format(self.term, self.course), logger)
        clear_prof_data()
        return json_obj

    def _explain(self, context, explanation):
        logger.debug("explain {}: {}".format(context, explanation))

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')
        ordering = ['-term__year', '-term__quarter']

    def __str__(self):
        return "{}-{}".format(self.term, self.course)
