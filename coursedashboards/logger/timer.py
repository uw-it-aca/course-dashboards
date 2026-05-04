# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime, timezone


class Timer:
    def __init__(self):
        """ Start the timer """
        self.start = self._now()

    def _now(self):
        return datetime.now(timezone.utc)

    def get_elapsed(self):
        """ Return the time spent in milliseconds """
        delta = self._now() - self.start
        return delta.microseconds / 1000.0
