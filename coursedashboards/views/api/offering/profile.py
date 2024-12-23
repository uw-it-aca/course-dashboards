# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.views.api import UpStreamErrorException
from coursedashboards.dao.pds import get_students_by_uwnetids
import logging

logger = logging.getLogger(__name__)

# https://studentdata.washington.edu/sdb-code-manual/
#   admissions/sdb-application-type-codes/
APPLICATION_TYPE_2YR_TRANSFER = '2'
APPLICATION_TYPE_4YR_TRANSFER = '4'
TRANSFER_CODES = [APPLICATION_TYPE_2YR_TRANSFER, APPLICATION_TYPE_4YR_TRANSFER]

# https://studentdata.washington.edu/sdb-code-manual/
#   student/sdb-special-program-codes/
EOP_CODES = ['1', '2', '13', '14', '16', '17', '31', '32', '33']

# https://studentdata.washington.edu/sdb-code-manual/
#   student/sdb-scholarship-codes/
PROBATION_CODES = ['2', '3', '4', '7', '81', '82']


class CourseProfileData(CoDaEndpoint):
    def get_data(self, offering):
        eop = 0
        xfer = 0
        disability = 0
        probation = 0

        try:
            netids = list(offering.get_registrations().values_list(
                'user__uwnetid', flat=True))

            self.total_registrations = len(netids)

            for person in get_students_by_uwnetids(netids):
                eop += self._inc(self._is_eop, person, offering)
                xfer += self._inc(self._is_transfer, person, offering)
                disability += self._inc(self._is_disability, person, offering)
                probation += self._inc(self._on_probation, person, offering)

            return {
                'eop': {
                    'n': eop,
                    'total': self.total_registrations,
                    'percent': self._percent(eop)
                },
                'transfer': {
                    'n': xfer,
                    'total': self.total_registrations,
                    'percent': self._percent(xfer)
                },
                'disability': {
                    'n': disability,
                    'total': self.total_registrations,
                    'percent': self._percent(disability)
                },
                'probation': {
                    'n': probation,
                    'total': self.total_registrations,
                    'percent': self._percent(probation)
                }
            }
        except Exception as ex:
            logger.exception(f"person service: {ex}")
            raise UpStreamErrorException()

    def _is_disability(self, person, offering):
        return person.get('disability_ind')

    def _is_eop(self, person, offering):
        return str(person.get('special_program_code')) in EOP_CODES

    def _is_transfer(self, person, offering):
        return str(person.get('application_type_code')) in TRANSFER_CODES

    def _on_probation(self, person, offering):
        if person.get('latest_transcript'):
            return str(
                person.get('latest_transcript').get('scholarship_type')
            ) in PROBATION_CODES
        return False

    def _inc(self, test, person, offering):
        try:
            return 1 if test(person, offering) else 0
        except (KeyError, AttributeError) as ex:
            logger.error(f"pds client: {ex}")
            return 0

    def _percent(self, c):
        return 100 * float(c)/float(self.total_registrations) if (
            self.total_registrations > 0) else 0.0
