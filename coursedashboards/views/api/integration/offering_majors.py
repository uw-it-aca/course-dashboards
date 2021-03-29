# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse
from coursedashboards.views.api.integration.offering_info import\
    OfferingInfoView
import json


class OfferingMajors(OfferingInfoView):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id, num_majors):

        offering = self.get_offering(year, quarter, curriculum,
                                     course_number, section_id)

        if isinstance(offering, HttpResponse):
            return offering

        json_response = self.get_majors(offering, int(num_majors))
        return HttpResponse(json.dumps(json_response))

    def get_majors(self, offering, num_majors):
        json_obj = {}

        offering.set_json_current_student_majors(json_obj)

        response = {}
        majors = []
        for x in range(0, num_majors):
            majors.append(json_obj['current_student_majors'][x])

        response['current_student_majors'] = majors

        return response
