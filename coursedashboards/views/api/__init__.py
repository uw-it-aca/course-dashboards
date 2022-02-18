# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from coursedashboards.models import Term, Course, CourseOffering
from coursedashboards.views.error import _make_response, MYUW_DATA_ERROR


class CoDaAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def get_offering(self, year, quarter, curriculum, course_number,
                     section_id):
        try:
            term = Term.objects.get(year=year, quarter=quarter.lower())
            course = Course.objects.get(curriculum=curriculum.upper(),
                                        course_number=course_number,
                                        section_id=section_id.upper())
            offering = CourseOffering.objects.get(term=term, course=course)
            return offering

        except Term.DoesNotExist:
            return self.term_not_found()
        except Course.DoesNotExist:
            return self.course_not_found()
        except CourseOffering.DoesNotExist:
            return self.course_offering_not_found()

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):

        offering = self.get_offering(year, quarter, curriculum,
                                     course_number, section_id)

        if isinstance(offering, HttpResponse):
            return offering

        json_response = self.get_data(offering)

        return JsonResponse(json_response)

    def get_data(self, offering):
        raise NotImplementedError("You must define your get_data method to "
                                  "use it!")

    def data_error(self):
        return _make_response(MYUW_DATA_ERROR,
                              "Data not available due to an error")

    def term_not_found(self):
        return HttpResponse(content="Term not found!", status=543)

    def course_not_found(self):
        return HttpResponse(content="Course not found!", status=543)

    def course_offering_not_found(self):
        return HttpResponse(content="Course Offering not found!", status=543)
