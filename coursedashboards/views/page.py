import json
import re
import logging
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from coursedashboards.dao.term import get_current_quarter
from coursedashboards.dao.affiliation import get_all_affiliations
from coursedashboards.dao import get_netid_of_current_user
from coursedashboards.dao.pws import get_person_of_current_user
from coursedashboards.dao.instructor_schedule import get_instructor_schedule_by_term
from uw_sws.section import get_sections_by_instructor_and_term, get_section_by_label
from uw_sws.registration import get_active_registrations_by_section
from uw_sws.enrollment import enrollment_search_by_regid, get_grades_by_regid_and_term, get_enrollment_by_regid_and_term


#logger = logging.getLogger(__name__)

def page(request,
         context={},
         template='course-page.html'):
    #timer = Timer()
    netid = get_netid_of_current_user()
    if not netid:
        #log_invalid_netid_response(logger, timer)
        return "nope"#invalid_session()
    context["user"] = {
        "netid": netid,
        "session_key": request.session.session_key,
     }

    context["home_url"] = "/"
    context["err"] = None
    context["user"]["affiliations"] = get_all_affiliations(request)

    if ('year' not in context or context['year'] is None or
            'quarter' not in context and context['quarter'] is None):
        cur_term = get_current_quarter(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    
    #adding below so can get instructors schedule
    person = get_person_of_current_user()
    
    #WORKS ONLY WITH bill100 - NEED ERROR HANDLING WHEN NO COURSES
    #currently getting ALL data for EVERY section being taught...perhaps should only pull data when needed?
    #SEPARATE FUNCTION
    sections = get_sections_by_instructor_and_term(person, cur_term)
    context["sections"] = []
    for section in sections:
        cur_section = section.json_data()
        status = get_section_by_label(cur_section['section_label'])
        students = get_current_students(status)
        concurrent_courses = get_concurrent_courses_all_students(students, cur_section['curriculum_abbr'] + " " + cur_section['course_number'] + " " + cur_section['section_id'], cur_term)
        current_majors = get_majors_all_students(students, cur_term)
        section_status = status.json_data()
        context["sections"].append({
            'curriculum':cur_section['curriculum_abbr'],
            'course_number':cur_section['course_number'],
            'section_label':cur_section['section_label'],
            'section_id':cur_section['section_id'],
            'current_enrollment':section_status['current_enrollment'],
            'limit_estimate_enrollment':section_status['limit_estimate_enrollment'],
            'current_median':calc_median_gpa_enrolled(status, students),
            'concurrent_courses':concurrent_courses,
            'current_student_majors':current_majors
        })
    context["sections"] = json.dumps(list(context["sections"]), cls=DjangoJSONEncoder)
    
    
    return render(request, template, context)

def calc_median_gpa_enrolled(section, students):
    gpas = []
    for student in students:
        gpas.append(get_student_gpa(student))
    return median(gpas)

def get_current_students(section):
    students = []
    registrations = get_active_registrations_by_section(section)
    for registration in registrations:
        """
        #not available until uw_sws updated
        if registration.is_repeat:
            print "Repeat!"
        else:
            print "Not repeat!"
        """
        students.append(registration.person.json_data())
    return students

def get_majors_all_students(students, term):
    majors_dict = {}
    total_students = len(students)
    for student in students:
        major = get_student_major(student, term)
        for m in major:
            if majors_dict.has_key(m.full_name):
                majors_dict[m.full_name] += 1
            else: majors_dict[m.full_name] = 1
    sorted_majors = sorted(majors_dict, reverse=True, key=majors_dict.get)
    top_majors = []
    for sort in sorted_majors:
        top_majors.append({
            "major":sort,
            "percent_students":round((float(majors_dict[sort])/float(total_students))*100.0,2)
        })
    return top_majors

def get_student_major(student, term):
    enrollment = get_enrollment_by_regid_and_term(student["uwregid"], term)
    return enrollment.majors

def get_student_gpa(student):
    #get enrollments for this student then calculate GPA
    #for each enrollment, add up QtrGradePoints, and QtrGradedAttmp
    enrollments = enrollment_search_by_regid(student["uwregid"])
    grade_points = 0
    credits_attempted = 0
    for term in enrollments:
        grades = get_grades_by_regid_and_term(student["uwregid"], term)
        grade_points += grades.grade_points
        credits_attempted += grades.credits_attempted
    return grade_points / credits_attempted

def get_concurrent_courses_all_students(students, this_course, term):
    all_courses = []
    course_dict = {}
    total_students = len(students)
    for student in students:
        all_courses += get_concurrent_courses_by_student(student, term)
    for course in all_courses:
        if course != this_course:
            if course_dict.has_key(course):
                course_dict[course] += 1
            else:
                course_dict[course] = 1
    sorted_courses = sorted(course_dict, reverse=True, key=course_dict.get)
    top_courses = []
    for sort in sorted_courses:
        top_courses.append({
            "course":sort,
            "percent_students":round((float(course_dict[sort])/float(total_students))*100.0,2)
        })
    return top_courses

def get_concurrent_courses_by_student(student, term):
    grades = grades = get_grades_by_regid_and_term(student["uwregid"], term)
    concurrent_courses = []
    for course in grades.grades:
        concurrent_courses.append(course.section.curriculum_abbr + " " + course.section.course_number + " " + course.section.section_id)
    return concurrent_courses

def median(values):
    values = sorted(values)
    n = len(values)
    if n < 1:
        return 0
    if n%2==1:
        return values[n//2]
    else:
        return sum(values[n//2-1:n//2+1]) / 2.0