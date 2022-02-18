# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import datetime


class Timer:
    def __init__(self):
        """ Start the timer """
        self.start = self._now()

    def _now(self):
        return datetime.datetime.utcnow()

    def get_elapsed(self):
        """ Return the time spent in milliseconds """
        delta = self._now() - self.start
        return delta.microseconds / 1000.0
