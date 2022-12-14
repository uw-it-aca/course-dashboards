# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

from uw_sws.course import get_course_by_label


def get_gen_ed_reqs_for_offering(offering):
    """
    returns general education requirements for a given course offering
    """
    course_label = "{},{},{},{}/{}".format(
        offering.term.year, offering.term.quarter,
        offering.course.curriculum, offering.course.course_number,
        offering.course.section_id)
    course = get_course_by_label(course_label)
    return course.json_data()['general_education_requirements']
