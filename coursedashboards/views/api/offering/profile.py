# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from uw_sws.models import Term
from uw_person_client.clients.mock_client import MockedUWPersonClient
from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
import math
import os


class CoDaUWPersonClient(UWPersonClient):
    def get_persons_by_uwnetids(
            self, uwnetids, page=None, page_size=None, **kwargs):
        sqla_persons = self.DB.session.query(self.DB.Person).filter(
            self.DB.Person.uwnetid.in_(uwnetids))
        return self._get_page(sqla_persons,
                              self._map_person,
                              page=page,
                              page_size=page_size,
                              **kwargs)


class CourseProfileData(CoDaEndpoint):
    # https://studentdata.washington.edu/sdb-code-manual/
    #     student/sdb-special-program-codes/
    EOP_CODES = ['1', '2', '13', '14', '16', '17', '31', '32', '33']

    # https://studentdata.washington.edu/sdb-code-manual/
    #     student/sdb-scholarship-codes/
    PROBATION_CODES = ['2', '3', '4', '7', '81', '82']

    def get_data(self, offering):
        eop = 0
        xfer = 0
        disability = 0
        probation = 0

        client = MockedUWPersonClient() if (
            os.getenv('ENV') == "localdev") else UWPersonClient()

        for r in offering.get_registrations():
            try:
                person = client.get_person_by_uwnetid(r.user.uwnetid)
            except PersonNotFoundException:
                continue

            try:
                if person.student.disability_ind:
                    disability += 1
            except KeyError:
                pass

            try:
                if str(person.student.special_program_code) in self.EOP_CODES:
                    eop += 1
            except KeyError:
                pass

            try:
                if len(person.student.transfers):
                    xfer += 1
            except KeyError:
                pass

            try:
                if self._on_probation(
                        offering.term, person.student.transcripts):
                    probation += 1
            except KeyError:
                pass

        return {
            'eop-percent': self._percent(eop, offering),
            'transfer-percent': self._percent(xfer, offering),
            'disability-percent': self._percent(disability, offering),
            'probation-percent': self._percent(probation, offering)
        }

    def _on_probation(self, term, transcripts):
        term_key = self._term_key(
            term.year, Term._quarter_to_int(term.quarter))
        transcript_terms = {}
        for i, transcript in enumerate(transcripts):
            transcript_terms[self._term_key(
                transcript.tran_term.year, transcript.tran_term.quarter)] = i

        for term in sorted(
                transcript_terms.items(), key=lambda x: x[0], reverse=True):
            if term[0] < term_key:
                transcript = transcripts[term[1]]
                return str(transcript.scholarship_type) in self.PROBATION_CODES

        return False

    def _percent(self, c, offering):
        return 100 * float(c)/float(offering.current_enrollment) if (
            offering.current_enrollment > 0) else 0.0

    def _term_key(self, year, quarter):
        return year * 10 + quarter
