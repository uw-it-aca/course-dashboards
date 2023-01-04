# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Contains the custom exceptions used by the restclients.
"""


class EmailServiceUrlException(Exception):
    """Unhandled email domain or malformed email address"""
    pass


class CanvasNonSWSException(Exception):
    """Non-academic (adhoc) Canvas course"""
    pass


class NotSectionInstructorException(Exception):
    """Request for section data from non-instructor"""
    pass


class CourseRequestEmailRecipientNotFound(Exception):
    """MAILMAN_COURSEREQUEST_RECIPIENT not in Settings"""
    pass


class IndeterminateCampusException(Exception):
    """Cannot determine campus from registrations or PWS"""
    pass


class MalformedOrInconsistentUser(Exception):
    """Cannot determine campus from registrations or PWS"""
    pass


class MissingNetIDException(Exception):
    """Missing or Invalid NetID"""
    pass


class NoTermAfterCurrent(Exception):
    """No course data for term after current"""
    pass
