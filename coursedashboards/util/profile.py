# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import time
from django.conf import settings
from functools import wraps


PROF_DATA = {}


def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        if not getattr(settings, 'CODA_PROFILE', False):
            return fn(*args, **kwargs)

        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in PROF_DATA:
            PROF_DATA[fn.__name__] = [1, [elapsed_time]]
        else:
            PROF_DATA[fn.__name__][0] += 1
            PROF_DATA[fn.__name__][1].append(elapsed_time)

        return ret

    return with_profiling


def log_profile_data(prefix, logger):
    for fname, data in list(PROF_DATA.items()):
        logger.debug(
            f"profile {prefix}: called:{data[0]:6}  max: {max(data[1]):.3f}"
            f" avg: {(sum(data[1]) / len(data[1])):.3f} {fname}")


def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}
