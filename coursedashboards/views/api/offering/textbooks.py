# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging

from coursedashboards.dao.textbook import get_books_for_offering
from coursedashboards.views.api import UpStreamErrorException
from coursedashboards.views.api.endpoint import CoDaEndpoint

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
        except Exception:
            logger.exception("bookstore service")
            raise UpStreamErrorException()
