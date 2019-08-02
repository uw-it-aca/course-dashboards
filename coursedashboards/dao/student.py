from coursedashboards.models import CourseMedianGPA
from uw_sws.enrollment import get_grades_by_regid_and_term, \
    get_enrollment_by_regid_and_term, enrollment_search_by_regid
from uw_sws.models import Term
from uw_sws.person import get_person_by_regid
from uw_sws.registration import get_active_registrations_by_section

"""
Gets data about students e.g. students enrolled
in course X, students' majors and GPAs
"""


def get_students_in_section(section):
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


def get_concurrent_sections_all_students(students,
                                         curriculum, course_number,
                                         section_id, term):
    all_courses = []
    course_dict = {}

    this_course = curriculum + " " + course_number + " " + section_id
    total_students = len(students)

    for student in students:
        all_courses += get_concurrent_sections_by_student(student, term)

    for course in all_courses:
        if course != this_course:
            if course in course_dict:
                course_dict[course] += 1
            else:
                course_dict[course] = 1

    sorted_courses = sorted(course_dict, reverse=True, key=course_dict.get)
    top_courses = []

    for sort in sorted_courses:
        top_courses.append({
            "course": sort,
            "number_students": course_dict[sort],
            "percent_students":
                round(
                    (float(course_dict[sort]) / float(total_students)) *
                    100.0, 2)
        })

    return top_courses


def get_concurrent_sections_by_student(student, term):
    grades = get_grades_by_regid_and_term(student["uwregid"], term)
    concurrent_courses = []

    for course in grades.grades:
        concurrent_courses.append(
            course.section.curriculum_abbr +
            " " + course.section.course_number +
            " " + course.section.section_id)

    return concurrent_courses


def get_majors_all_students(students, term):
    majors_dict = {}
    total_students = len(students)

    for student in students:
        major = get_student_major(student, term)
        for m in major:
            if m.full_name in majors_dict:
                majors_dict[m.full_name] += 1
            else:
                majors_dict[m.full_name] = 1

    return order_majors(majors_dict, total_students)


def get_most_recent_majors_all_students(students):
    majors_dict = {}
    total_students = len(students)

    for student in students:
        person = get_person_by_regid(student["uwregid"])

        term = Term()
        term.quarter = person.last_enrolled.quarter
        term.year = person.last_enrolled.year

        majors = get_student_major(student, term)

        for m in majors:
            if m.full_name in majors_dict:
                majors_dict[m.full_name] += 1
            else:
                majors_dict[m.full_name] = 1

    return order_majors(majors_dict, total_students)


def get_student_major(student, term):
    """

    :param student:
    :param term:
    :return:
    """
    enrollment = get_enrollment_by_regid_and_term(student["uwregid"], term)

    return enrollment.majors


def calc_median_gpa(section, students):
    """

    :param section:
    :param students:
    :return:
    """
    saved_value = CourseMedianGPA.get_cached(section)

    if saved_value:
        return saved_value

    gpas = []

    for student in students:
        gpas.append(get_student_gpa(student))
    new_value = median(gpas)

    CourseMedianGPA.save_value(section, new_value)

    return new_value


def get_student_gpa(student):
    """
    Get enrollments for this student then calculate GPA for each enrollment,
    add up QtrGradePoints, and QtrGradedAttmp
    :param student: an SWS Student object
    :return:
    """
    #
    #

    enrollments = enrollment_search_by_regid(student["uwregid"])
    grade_points = 0
    credits_attempted = 0

    for term in enrollments:
        grades = get_grades_by_regid_and_term(student["uwregid"], term)
        grade_points += count_numeric_only(grades.grade_points)
        credits_attempted += count_numeric_only(grades.credits_attempted)

    return grade_points / credits_attempted


def count_numeric_only(num):
    try:
        ret = float(num)
        return ret
    except TypeError:
        return 0


# PLACEHOLDER until SWS client is updated
def get_all_course_grades(section):
    students = get_active_registrations_by_section(section)
    for student in students:
        student.grade = 3.5
    # ADD WHEN SWS CLIENT UPDATED print student.grade
    return students


def median(values):
    values = sorted(values)
    n = len(values)
    if n < 1:
        return 0
    if n % 2 == 1:
        return values[n//2]
    else:
        return sum(values[n//2-1:n//2+1]) / 2.0
