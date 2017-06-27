import json
from django.core.serializers.json import DjangoJSONEncoder
from uw_sws.section import get_sections_by_instructor_and_term,\
    get_section_by_label, get_section_by_url
from coursedashboards.dao.student import get_students_in_section,\
    get_concurrent_sections_all_students, get_majors_all_students,\
    calc_median_gpa

quarter = ["winter", "spring", "summer", "autumn"]


def get_past_offering_of_course(curriculum, course_number, start_term,
                                years=5, min_offerings=2):
    # search for past offerings of course up to x years ago,
    # need to find at least min_offerings in order to display data
    course_prefix = "/student/v5/course/"
    start_quarter = quarter.index(start_term.quarter)
    furthest_quarter = start_quarter + 1 if (start_quarter < 4) else 0
    furthest_year = start_term.year - years if (furthest_quarter > 0)\
        else start_term.year - (years-1)
    # loop backwards through time
    url = course_prefix + str(start_term.year) + "," + start_term.quarter\
        + "," + curriculum + "," + course_number + "/A.json"
    return get_section_by_url(url).json_data()


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
        print past_offerings
        con_sections.append({
            'curriculum': cur_section['curriculum_abbr'],
            'course_number': cur_section['course_number'],
            'section_label': cur_section['section_label'],
            'section_id': cur_section['section_id'],
            'current_enrollment': section_status['current_enrollment'],
            'limit_estimate_enrollment':
                section_status['limit_estimate_enrollment'],
            'current_median': calc_median_gpa(students),
            'concurrent_courses': concurrent_sections,
            'current_student_majors': current_majors,
            'past_offerings': past_offerings
        })
    con_sections = json.dumps(list(con_sections), cls=DjangoJSONEncoder)
    return con_sections


def get_instructor_current_sections(person, term):
    return get_sections_by_instructor_and_term(person, term)
