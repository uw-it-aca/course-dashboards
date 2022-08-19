# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.views.api import UpStreamErrorException
from uw_person_client.clients.mock_client import MockedUWPersonClient
from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
import logging
import os


logger = logging.getLogger(__name__)


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
    def get_data(self, offering):
        eop = 0
        xfer = 0
        disability = 0
        probation = 0

        client = MockedUWPersonClient() if (
            os.getenv('ENV') == "localdev") else UWPersonClient()

        try:
            regs = offering.get_registrations()
            self.total_registrations = len(regs)
            for r in regs:
                try:
                    person = client.get_person_by_uwnetid(r.user.uwnetid)
                except PersonNotFoundException:
                    logger.error("person service netid not found: {}".format(
                        r.user.uwnetid))
                    raise

                eop += self._inc(self._is_eop, person, offering)
                xfer += self._inc(self._is_transfer, person, offering)
                disability += self._inc(self._is_disability, person, offering)
                probation += self._inc(self._on_probation, person, offering)

            return {
                'eop': {
                    'n': eop,
                    'percent': self._percent(eop)
                },
                'transfer': {
                    'n': xfer,
                    'percent': self._percent(xfer)
                },
                'disability': {
                    'n': disability,
                    'percent': self._percent(disability)
                },
                'probation': {
                    'n': probation,
                    'percent': self._percent(probation)
                }
            }
        except Exception as ex:
            logger.exception("person service: {}".format(ex))
            raise UpStreamErrorException()

    def _is_disability(self, person, offering):
        return person.student.disability_ind

    def _is_eop(self, person, offering):
        # https://studentdata.washington.edu/sdb-code-manual/
        #     student/sdb-special-program-codes/
        EOP_CODES = ['1', '2', '13', '14', '16', '17', '31', '32', '33']

        return str(person.student.special_program_code) in EOP_CODES

    def _is_transfer(self, person, offering):
        return len(person.student.transfers) > 0

    def _on_probation(self, person, offering):
        # https://studentdata.washington.edu/sdb-code-manual/
        #     student/sdb-scholarship-codes/
        PROBATION_CODES = ['2', '3', '4', '7', '81', '82']

        transcript_terms = {}
        for i, transcript in enumerate(person.student.transcripts):
            tran_key = (
                transcript.tran_term.year * 10) + transcript.tran_term.quarter
            transcript_terms[tran_key] = i

        for term in sorted(
                transcript_terms.items(), key=lambda x: x[0], reverse=True):
            if term[0] < offering.term.term_key:
                transcript = person.student.transcripts[term[1]]
                return str(transcript.scholarship_type) in PROBATION_CODES

        return False

    def _inc(self, test, person, offering):
        try:
            return 1 if test(person, offering) else 0
        except (KeyError, AttributeError):
            logger.exception("person reference")
            return 0

    def _percent(self, c):
        return 100 * float(c)/float(self.total_registrations) if (
            self.total_registrations > 0) else 0.0
