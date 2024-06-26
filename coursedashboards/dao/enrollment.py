# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from uw_sws.enrollment import get_enrollment_by_regid_and_term
from restclients_core.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def get_enrollment_for_regid_and_term(regid, term):
    return get_enrollment_by_regid_and_term(regid, term)


def get_student_majors_for_regid_and_term(regid, term):
    try:
        enrollment = get_enrollment_for_regid_and_term(regid, term)
        return enrollment.majors
    except DataFailureException as ex:
        if ex.status == 404:
            logger.info("Student_majors: no {} enrollments for {}: {}".format(
                term, regid, ex))
        else:
            logger.error("Student_majors: for {}: {}".format(regid, ex))
    except AttributeError as ex:
        logger.info(
            "Student_majors: No enrollments for {}: {}".format(regid, ex))
    except Exception as ex:
        logger.exception("Student_majors: for {}: {}".format(regid, ex))

    return []
