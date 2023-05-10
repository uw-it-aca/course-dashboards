# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.clients.mock_client import MockedUWPersonClient
from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
import os


class CoDaUWPersonClient():
    def __new__(self, *args, **kwargs):
        if (os.getenv('ENV') == "localdev"):
            return CoDaMockedUWPersonClient(*args, **kwargs)
        else:
            return CoDaLiveUWPersonClient(*args, **kwargs)


class CoDaLiveUWPersonClient(UWPersonClient):
    def get_persons_by_uwnetids(self, uwnetids, **kwargs):
        sqla_persons = self.DB.session.query(self.DB.Person).filter(
            self.DB.Person.uwnetid.in_(uwnetids))

        kwargs.update({
            'include_employee': False,
            'include_student': True,
            'include_student_transcripts': True,
            'include_student_transfers': True,
            'include_student_sports': False,
            'include_student_advisers': False,
            'include_student_majors': False,
            'include_student_pending_majors': False,
            'include_student_holds': False,
            'include_student_degrees': False})

        return [self._map_person(p, **kwargs) for p in sqla_persons.all()]

    def get_persons_by_uwregids(self, uwregids, **kwargs):
        sqla_persons = self.DB.session.query(self.DB.Person).filter(
            self.DB.Person.uwregid.in_(uwregids))
        return [self._map_person(p, **kwargs) for p in sqla_persons.all()]


class CoDaMockedUWPersonClient(MockedUWPersonClient):
    def get_persons_by_uwnetids(self, uwnetids):
        persons = []
        for netid in uwnetids:
            try:
                persons.append(self.get_person_by_uwnetid(netid))
            except PersonNotFoundException:
                print("person for netid not found: {}".format(netid))

        return persons
