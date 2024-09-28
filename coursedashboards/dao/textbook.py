# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

from uw_bookstore import Bookstore
from uw_sws.section import get_section_by_label


def get_books_for_offering(offering):
    """
    returns textbooks for a given course
    """
    section_label = (
        f"{offering.term.year},{offering.term.quarter},"
        f"{offering.course.curriculum},{offering.course.course_number}"
        f"/{offering.course.section_id}")
    section = get_section_by_label(section_label)
    return (section.sln, section.course_campus,
            Bookstore().get_books_by_quarter_sln(
                offering.term.quarter, section.sln))
