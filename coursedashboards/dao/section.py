import json

from django.core.serializers.json import DjangoJSONEncoder
from uw_sws.models import Term
from uw_sws.section import get_sections_by_instructor_and_term, \
    get_section_by_label
from coursedashboards.dao.student import get_students_in_section, \
    get_concurrent_sections_all_students, get_majors_all_students, \
    calc_median_gpa, get_most_recent_majors_all_students

quarter = ["winter", "spring", "summer", "autumn"]


def get_past_offering_of_course(curriculum, course_number, start_term,
                                years=5, min_offerings=2):
    # search for past offerings of course up to x years ago,
    # need to find at least min_offerings in order to display data

    course_prefix = "/student/v5/course/"
    start_quarter = quarter.index(start_term.quarter)
    test_quarter = start_quarter + 1 if (start_quarter < 4) else 0
    test_year = start_term.year - years if (test_quarter > 0)\
        else start_term.year - (years-1)

    # look for past offerings in each quarter
    # don't need to return full section info
    # create object containing section term info plus every student grade

    past_offerings = []
    grades = []

    while test_year <= start_term.year:
        """
        Can't get grades until sws rest client is updated
        try:
            section = get_section_by_label(str(test_year) + "," +
             quarter[test_quarter] + "," + curriculum + "," +
             str(course_number) + "/A")
            grades = get_all_course_grades(section)
            print grades
        except Exception as ex:
            msg = ex.args
            print msg
        """
        term = Term()
        term.quarter = quarter[test_quarter]
        term.year = test_year

        try:
            section = get_section_by_label(str(test_year) + "," +
                                           quarter[test_quarter] +
                                           "," + curriculum + "," +
                                           str(course_number) + "/A")
            students = get_students_in_section(section)

            past_offerings.append({
                "year": test_year,
                "quarter": quarter[test_quarter],
                "majors": get_majors_all_students(students, term),
                "concurrent_courses":
                    get_concurrent_sections_all_students(students, curriculum,
                                                         course_number, "A",
                                                         term),
                "instructors": get_instructors_for_section(section),
                "latest_majors": get_most_recent_majors_all_students(students)
            })

        except Exception as ex:
            msg = ex.args

        if test_quarter == 3:
            test_year += 1
            test_quarter = 0
        else:
            test_quarter += 1

        if (test_year == start_term.year and
                test_quarter == quarter.index(start_term.quarter)):
            break
    return past_offerings


def get_instructors_for_section(section):
    instructors = []
    netids = []

    for meeting in section.meetings:
        for instructor in meeting.instructors:
            if instructor.uwnetid not in netids and instructor.uwnetid:

                instructors.append({
                    'display_name': instructor.display_name,
                    'uwnetid': instructor.uwnetid
                })

                netids.append(instructor.uwnetid)

    return instructors


def create_sections_context(sections, term):
    con_sections = []

    for section in sections:
        cur_section = section.json_data()

        status = get_section_by_label(cur_section['section_label'])
        students = get_students_in_section(status)

        concurrent_sections = get_concurrent_sections_all_students(
            students, cur_section['curriculum_abbr'],
            cur_section['course_number'],
            cur_section['section_id'], term)

        current_majors = get_majors_all_students(students, term)
        section_status = status.json_data()

        past_offerings = get_past_offering_of_course(
            cur_section['curriculum_abbr'],
            cur_section['course_number'], term)

        con_sections.append({
            'curriculum': cur_section['curriculum_abbr'],
            'course_number': cur_section['course_number'],
            'section_label': cur_section['section_label'],
            'section_id': cur_section['section_id'],
            'current_enrollment': section_status['current_enrollment'],
            'limit_estimate_enrollment':
                section_status['limit_estimate_enrollment'],
            'current_median': calc_median_gpa(section, students),
            'concurrent_courses': concurrent_sections,
            'current_student_majors': current_majors,
            'past_offerings': past_offerings
        })

    con_sections = json.dumps(list(con_sections), cls=DjangoJSONEncoder)

    return con_sections


def get_instructor_current_sections(person, term):
    return get_sections_by_instructor_and_term(person, term)
