# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from persistent_message.models import Message


def get_persistent_messages(tags="", params={}):
    ret = {}
    for message in Message.objects.active_messages(tags=tags):
        level = message.get_level_display().lower()
        message = message.render(params)
        try:
            ret[level].append(message)
        except KeyError:
            ret[level] = [message]
    print("RETURNING MESSAGES: {} ".format(ret))
    return ret
