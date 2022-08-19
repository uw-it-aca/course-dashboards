# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.dao import MockDAO
from uw_person_client.clients.mock_client import MockedUWPersonClient
from os.path import join, abspath, dirname

MockDAO.register_mock_path(join(abspath(dirname(__file__)), "resources"))

try:
    MockedUWPersonClient.register_mock_path(join(
        abspath(dirname(__file__)), "resources/uw_person_client/fixtures"))
except:
    pass
