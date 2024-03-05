# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.views.api import UpStreamErrorException
from coursedashboards.dao.textbook import get_books_for_offering
import logging


logger = logging.getLogger(__name__)


class CourseTextbookData(CoDaEndpoint):
    def get_data(self, offering):
        try:
            sln, campus, books = get_books_for_offering(offering)
            return {
                'sln': sln,
                'campus': campus,
                'textbooks': [book.isbn for book in books]
            }
        except Exception as ex:
            logger.exception("bookstore service: {}".format(ex))
            raise UpStreamErrorException()
