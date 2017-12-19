

import json
from threading import Thread

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering, Course, Term
from coursedashboards.views.api.course_info import CourseInfoView


class CourseData(CourseInfoView):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id):
        try:
            offering = self.get_offering(year, quarter, curriculum,
                                         course_number, section_id)
        except Term.DoesNotExist:
            return self.term_not_found()
        except Course.DoesNotExist:
            return self.course_not_found()
        except CourseOffering.DoesNotExist:
            return self.course_offering_not_found()

        json_response = self.get_data(offering)
        return HttpResponse(json.dumps(json_response))

    def get_data(self, offering):
        if offering.current_enrollment <= 5:
            return json.dumps(offering.base_json_object())

        return json.dumps(offering.json_object())

