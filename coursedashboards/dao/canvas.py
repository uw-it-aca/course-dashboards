# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from uw_canvas.courses import Courses as CanvasCourses
from restclients_core.exceptions import DataFailureException
from uw_sws.exceptions import InvalidCanvasIndependentStudyCourse
from coursedashboards.util.retry import retry


logger = logging.getLogger(__name__)


@retry(DataFailureException, status_codes=[408, 500, 502, 503, 504],
       tries=5, delay=3, logger=logger)
def canvas_course_url_from_section(section):
    try:
        sis_id = section.canvas_course_sis_id()
        canvas_course = CanvasCourses().get_course_by_sis_id(sis_id)
        return canvas_course.course_url
    except DataFailureException as ex:
        if ex.status == 404:
            logger.info("no canvas course: {}".format(sis_id))
        else:
            logger.error("problem with canvas: {}".format(ex))
    except InvalidCanvasIndependentStudyCourse as ex:
        logger.error("problem with canvas: {}".format(ex))
    except Exception as ex:
        logger.error("problem with canvas: {}".format(ex))

    return ''
