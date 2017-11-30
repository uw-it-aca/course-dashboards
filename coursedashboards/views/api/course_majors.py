import json
from threading import Thread

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering, Term, Course
from coursedashboards.views.api.course_info import CourseInfoView


class CourseMajors(CourseInfoView):

    def get(self, request, year, quarter, curriculum, course_number,
            section_id, num_majors):
        try:
            offering = self.get_offering(year, quarter, curriculum,
                                         course_number, section_id)
        except Term.DoesNotExist:
            return self.term_not_found()
        except Course.DoesNotExist:
            return self.course_not_found()
        except CourseOffering.DoesNotExist:
            return self.course_offering_not_found()

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
