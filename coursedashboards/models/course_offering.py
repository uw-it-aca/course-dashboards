from django.conf import settings
from django.db.models import (
    Count, Sum, F, Avg, Subquery, OuterRef, FloatField, Value)
from django.db.models.functions import Concat
from statistics import median
from statistics import StatisticsError
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
    def get_registrations(self, terms=None, is_alum=None):
        """
        Return Registration queryset for this course offering
        """
        filter_parms = self._filter_parms(terms, is_alum)
        return Registration.objects.filter(filter_parms)

    @profile
    def _filter_parms(self, terms=None, is_alum=None):
        term_filter = models.Q(course=self.course)

        if terms:
            term_filter &= models.Q(term__in=terms)
        else:
            term_filter &= models.Q(term=self.term)

        if is_alum:
            term_filter &= models.Q(user__is_alum=1)

        return term_filter

    @profile
    def get_students(self, terms=None, is_alum=False):
        return self.get_registrations(
            terms,
            is_alum
        ).values_list(
            'user_id', flat=True
        )

    @profile
    def get_instructors(self, terms=None):
        filter_parms = self._filter_parms(terms)
        return Instructor.objects.filter(filter_parms)

    @profile
    def get_student_count(self, terms=None):
        return float(self.get_registrations(terms=terms).count())

    @profile
    def get_gpas(self, terms=None):
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
    def get_enrollment_count(self, terms=None, is_alum=None):
        filter_parms = self._filter_parms(terms, is_alum)

        return CourseOffering.objects.filter(
            filter_parms
        ).aggregate(
            Sum('current_enrollment')
        )['current_enrollment__sum']

    @profile
    def all_student_registrations(self, terms=None):
        """
        Return given user's Courses for this term
        """
        return Registration.objects.filter(
            term__in=terms if terms else [self.term],
            user_id__in=self.get_students(terms)
        ).select_related(
            'course'
        )

    def _course_id(self, course):
        return "{}-{}".format(course.curriculum, course.course_number)

    @profile
    def concurrent_courses(self, terms=None):
        # all courses students in this offering for the given term
        # are registered
        students = self.get_students(terms=terms)
        student_count = float(students.distinct().count())
        registrations = Registration.objects.filter(
            user_id__in=students
        ).exclude(
            course=self.course
        )

        return list(registrations.annotate(
            title=F('course__course_title'),
            curriculum=F('course__curriculum'),
            course_number=F('course__course_number'),
            course_ref=Concat('course__curriculum', Value('-'),
                              'course__course_number',
                              output_field=models.CharField())
        ).values(
            'title',
            'curriculum',
            'course_number',
            'course_ref'
        ).annotate(
            course_students=Count('course_ref'),
            percent_students=Count('course_ref') * 100.0 / student_count
        ).order_by(
            '-percent_students')[:20])

    @profile
    def student_majors_for_term(self, terms=None):
        return self.student_major_distribution(terms)

    @profile
    def last_student_undergraduate_major(self, terms=None):
        return self.student_major_distribution(terms, graduated_major=True)

    @profile
    def student_major_distribution(self, terms=None, graduated_major=False):
        major_filter = {
            'user_id__in': self.get_students(
                terms=terms, is_alum=(graduated_major is True))
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
                percent_students=((Count('major') * 100.0 / majors_count))
            ).order_by(
                '-percent_students'
            )[:20])

    @profile
    def get_graduated_majors(self, terms=None):
        return self.last_student_undergraduate_major(terms)

    @profile
    def get_majors(self, terms=None):
        return self.student_majors_for_term(terms)

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
    def set_past_course_grades(self, past_obj, terms=None):
        past_obj['course_grades'] = self.get_grades(terms)

    @profile
    def set_past_median_gpa(self, past_obj, terms=None):
        past_obj['gpas'] = self.get_gpas(terms)

    @profile
    def set_past_offering_performance_data(self, past_obj, terms):
        threads = []

        t = Thread(target=self.set_past_course_grades,
                   args=(past_obj, terms,))
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
    def get_past_sections(self, terms=None):
        """
        List of past course sections
        """
        sections = {}
        for i in self.get_instructors(terms):
            if i.term.year not in sections:
                sections[i.term.year] = {}

            if i.term.quarter not in sections[i.term.year]:
                sections[i.term.year][i.term.quarter] = []

            sections[i.term.year][i.term.quarter].append(i.user.to_json())

        return sections

    @profile
    def get_past_offerings(self, terms):
        """
        List of past course offerings
        """
        return {
            'enrollment': self.get_enrollment_count(terms),
            'terms': [
                "{}".format(t) for t in Term.objects.filter(id__in=terms)]
        }

    @profile
    def get_past_offerings_performance_data(self, terms):
        """
        Past offerings course performance data
        """
        offerings = {
            'enrollment': self.get_enrollment_count(terms),
            'offering_count': len(terms)
        }

        self.set_past_offering_performance_data(offerings, terms)

        return offerings

    def _terms_from_search_filter(
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

        term_ids = Instructor.objects.filter(
            filter_parms
        ).exclude(
            term=self.term
        ).values_list(
            'term', flat=True
        ).distinct()

        # by policy, only select past 20 terms (5 years)
        oldest_term_year = self.term.year - 5
        try:
            last_term = Term.objects.get(
                year=oldest_term_year, quarter=self.term.quarter)
        except Term.DoesNotExist:
            last_term = Term.objects.create(
                year=oldest_term_year, quarter=self.term.quarter)

        return [t.id for t in sorted(
            Term.objects.filter(id__in=term_ids), reverse=True) if (
                t >= last_term)]

    def past_offerings_json_object(
            self, past_year='', past_quarter='', instructor=None):
        terms = self._terms_from_search_filter(
            past_year, past_quarter, instructor)

        json_obj = {
            'past_offerings': self.get_past_offerings(terms),
            'sections': self.get_past_sections(terms),
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
            'performance': self.get_past_offerings_performance_data(terms),
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
            'concurrent_courses': self.concurrent_courses(terms),
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
            'student_majors': self.get_majors(terms),
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
