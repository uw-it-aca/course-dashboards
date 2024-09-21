# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.db.models import Q, Count, Sum, F
from django.db.models.functions import Round
from statistics import median
from statistics import StatisticsError
from collections import Counter
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
from uw_sws.term import get_current_term
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
    def get_registrations(self, terms=None, is_alum=None, instructor=None):
        """
        Return Registration queryset for this course offering
        """
        filter_parms = self._filter_parms(
            terms=terms, is_alum=is_alum, instructor=instructor)
        return Registration.objects.filter(filter_parms)

    @profile
    def _filter_parms(self, terms=None, is_alum=None, instructor=None):
        if instructor:
            # implies cross-term historic query
            term_filter = Q(term__in=[])

            for term in terms:
                instructed = Instructor.objects.instructed(
                    instructor, term, self.course)

                term_filter |= Q(term__id=term, course__id__in=instructed)
        elif terms:
            # implies cross-term, cross-section  historic query
            term_filter = (
                Q(term__in=terms)
                & Q(course__curriculum=self.course.curriculum)
                & Q(course__course_number=self.course.course_number))
        else:
            # only this offering's term and course section
            term_filter = Q(term=self.term) & Q(course=self.course)

        if is_alum:
            term_filter &= Q(user__is_alum=1)

        return term_filter

    @profile
    def get_students(self, terms=None, is_alum=False, instructor=False):
        return self.get_registrations(
            terms=terms, is_alum=is_alum, instructor=instructor
        ).values_list(
            'user_id', flat=True
        )

    @profile
    def get_instructors(self, terms=None, instructor=None):
        filter_parms = self._filter_parms(terms=terms, instructor=instructor)
        return Instructor.objects.filter(filter_parms)

    @profile
    def get_gpas(self, terms=None, instructor=None):
        registrations = Registration.objects.filter(
            user_id__in=self.get_students(terms=terms, instructor=instructor),
            term_id__in=[t.id for t in Term.objects.all() if t < self.term]
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
    def get_grades(self, terms=None, instructor=None):
        """
        Return grade array for course offering
        """
        return [float(grade) for grade in list(
            self.get_registrations(
                terms=terms, instructor=instructor
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
    def get_enrollment_count(self, terms=None, instructor=None):
        filter_parms = self._filter_parms(terms=terms, instructor=instructor)

        return CourseOffering.objects.filter(
            filter_parms
        ).aggregate(
            Sum('current_enrollment')
        )['current_enrollment__sum']

    @profile
    def concurrent_courses(self, terms=None, instructor=None):
        total_students = 0
        all_courses = {}

        # collect concurrent courses by term, summing student counts
        for term in terms if terms else [self.term]:
            filter_parms = self._filter_parms(
                terms=[term] if terms else None, instructor=instructor)
            user_ids = list(Registration.objects.values_list(
                'user_id', flat=True).filter(filter_parms).distinct())

            total_students += len(user_ids)

            courses = Registration.objects.values(
                'course_id',
                'course__curriculum',
                'course__course_number').annotate(
                    course_students=Count('course_id')).filter(
                        term_id=term,
                        user__id__in=user_ids).order_by(
                            '-course_students')[:100]

            for course in courses:
                course_id = course.get('course_id')
                curriculum = course.get('course__curriculum')
                course_number = course.get('course__course_number')

                if (curriculum == self.course.curriculum
                        and course_number == self.course.course_number):
                    continue

                try:
                    all_courses[course_id][
                        'enrollments'] += course.get('course_students')
                except KeyError:
                    all_courses[course_id] = {
                        'curriculum': curriculum,
                        'course_number': course_number,
                        'enrollments': course.get('course_students')}

        return [{
            'course_ref': f'{c[1]['curriculum']}-{c[1]['course_number']}',
            'curriculum': c[1]['curriculum'],
            'course_number': c[1]['course_number'],
            'course_students': c[1]['enrollments'],
            'percent_students': (c[1]['enrollments'] * 100.0) / total_students
        } for c in sorted(
            all_courses.items(), key=lambda x: x[1]['enrollments'],
            reverse=True)[:20]]

    @profile
    def student_majors_for_term(self, terms=None, instructor=None):
        return self.student_major_distribution(
            terms=terms, instructor=instructor)

    @profile
    def last_student_undergraduate_major(self, terms=None, instructor=None):
        return self.student_major_distribution(
            terms=terms, instructor=instructor, graduated_major=True)

    @profile
    def student_major_distribution(
            self, terms=None, instructor=None, graduated_major=False):
        major_filter = {
            'user_id__in': self.get_students(
                terms=terms, instructor=instructor,
                is_alum=(graduated_major is True))
        }

        if graduated_major:
            major_filter['major__degree_level'] = 1
        else:
            major_filter['term__in'] = terms if terms else [self.term]

        majors = StudentMajor.objects.filter(**major_filter)
        majors_count = float(majors.count())

        return list(
            majors.annotate(
                major_name=F('major__major')
            ).values(
                'major_name'
            ).annotate(
                percent_students=Round(
                    (Count('major') * 100.0) / majors_count)
            ).order_by(
                '-percent_students'
            )[:20])

    @profile
    def get_graduated_majors(self, terms=None):
        return self.last_student_undergraduate_major(terms)

    @profile
    def get_majors(self, terms=None, instructor=None):
        return self.student_majors_for_term(terms=terms, instructor=instructor)

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
        json_obj[
            'median_course_grade'] = self.get_cumulative_median_gpa(grades)

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
    def set_past_course_grades(self, past_obj, terms=None, instructor=None):
        past_obj['course_grades'] = self.get_grades(terms, instructor)

    @profile
    def set_past_median_gpa(self, past_obj, terms=None):
        past_obj['gpas'] = self.get_gpas(terms)

    @profile
    def set_past_offering_performance_data(self, past_obj, terms, instructor):
        threads = []

        t = Thread(target=self.set_past_course_grades,
                   args=(past_obj, terms, instructor,))
        threads.append(t)
        t.start()

        if bool(getattr(settings, "HISTORIC_CGPA_ENABLED", True)):
            t = Thread(target=self.set_past_median_gpa,
                       args=(past_obj, terms,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    @profile
    def get_past_sections(self, terms=None, instructor=None):
        """
        List of past course sections
        """
        sections = {}
        seen = {}
        for i in self.get_instructors(terms, instructor):
            if i.term.year not in sections:
                sections[i.term.year] = {}

            if i.term.quarter not in sections[i.term.year]:
                sections[i.term.year][i.term.quarter] = []

            # filter duplicates
            if i.user.id not in seen:
                seen[i.user.id] = {i.term.year: [i.term.quarter]}
            elif i.term.year not in seen[i.user.id]:
                seen[i.user.id][i.term.year] = [i.term.quarter]
            elif i.term.quarter not in seen[i.user.id][i.term.year]:
                seen[i.user.id][i.term.year].append(i.term.quarter)
            else:
                continue

            sections[i.term.year][i.term.quarter].append(i.user.to_json())

        return sections

    @profile
    def get_past_offerings(self, terms, instructor):
        """
        List of past course offerings
        """
        return {
            'enrollment': self.get_enrollment_count(
                terms=terms, instructor=instructor),
            'terms': [
                "{}".format(t) for t in Term.objects.filter(id__in=terms)]
        }

    @profile
    def get_past_offerings_performance_data(self, terms, instructor):
        """
        Past offerings course performance data
        """
        offerings = {
            'enrollment': self.get_enrollment_count(
                terms=terms, instructor=instructor),
            'offering_count': len(terms)
        }

        self.set_past_offering_performance_data(offerings, terms, instructor)

        return offerings

    def _terms_from_search_filter(
            self, past_year='', past_quarter='', instructor=None):
        # build filter for past offerings
        filter_parms = Q(course__curriculum=self.course.curriculum,
                         course__course_number=self.course.course_number)

        if past_year:
            filter_parms &= Q(term__year=int(past_year))

        if past_quarter:
            quarter = past_quarter.lower()
            if quarter in ['winter', 'spring', 'summer', 'autumn']:
                filter_parms &= Q(term__quarter=quarter)

        if instructor:
            filter_parms &= Q(user=instructor.id)

        term_ids = Instructor.objects.filter(
            filter_parms
        ).exclude(
            term=self.term
        ).values_list(
            'term', flat=True
        ).distinct()

        # by policy, only select past 20 terms (5 years)
        current_sws_term = get_current_term()
        current_term, created = Term.objects.get_or_create(
            year=current_sws_term.year, quarter=current_sws_term.quarter)

        oldest_term_year = current_term.year - 5
        last_term, created = Term.objects.get_or_create(
            year=oldest_term_year, quarter=current_term.quarter)

        return [t.id for t in sorted(
            Term.objects.filter(id__in=term_ids), reverse=True) if (
                t < current_term and t >= last_term)]

    def past_offerings_json_object(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        json_obj = {
            'past_offerings': self.get_past_offerings(terms, instructor),
            'sections': self.get_past_sections(terms, instructor),
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

    def past_offerings_performance_data(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        json_obj = {
            'performance': self.get_past_offerings_performance_data(
                terms, instructor),
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

    @profile
    def past_offerings_concurrent_courses(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        return {
            'concurrent_courses': self.concurrent_courses(
                terms, instructor),
            'filter': {
                'year': past_year,
                'quarter': past_quarter,
                'only_instructed': instructor is not None
            }
        }

    @profile
    def past_offerings_course_gpas(self, courses):
        gpas = []
        for course in courses.split(','):
            try:
                cur, num = course.split('-')
            except Exception:
                continue

            try:
                g = CourseGradeAverage.objects.get(
                    curriculum=cur, course_number=int(num))
                gpas.append({
                    'curriculum': cur,
                    'course_number': num,
                    'grade': g.grade
                })
            except CourseGradeAverage.DoesNotExist:
                pass

        return {
            'gpas': gpas
        }

    @profile
    def past_offerings_student_majors(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        return {
            'student_majors': self.get_majors(terms, instructor),
            'filter': {
                'year': past_year,
                'quarter': past_quarter,
                'only_instructed': instructor is not None
            }
        }

    @profile
    def past_offerings_graduated_majors(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        return {
            'graduated_majors': self.get_graduated_majors(terms),
            'filter': {
                'year': past_year,
                'quarter': past_quarter,
                'only_instructed': instructor is not None
            }
        }

    def _explain(self, context, explanation):
        logger.debug("explain {}: {}".format(context, explanation))

    class Meta:
        db_table = 'CourseOffering'
        unique_together = ('term', 'course')
        ordering = ['-term__year', '-term__quarter']

    def __str__(self):
        return "{}-{}".format(self.term, self.course)
