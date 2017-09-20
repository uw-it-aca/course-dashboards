import json

from django.core.serializers.json import DjangoJSONEncoder
from uw_sws.section import get_section_by_label
from coursedashboards.dao.student import get_students_in_section, \
    get_concurrent_sections_all_students, get_majors_all_students, \
    calc_median_gpa, get_most_recent_majors_all_students


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

        past_offerings = {}

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
