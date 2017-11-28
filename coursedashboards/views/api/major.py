from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering


class CourseSummary(APIView):

    def get(self, request):


        course_offering = CourseOffering()

        summary = self.majors(course_offering)

    def majors(self, offering, num_majors):
        json_obj = {}

        threads = []

        t = Thread(target=offering.set_json_current_student_majors,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t.join()
        response = {}
        majors = []
        for x in range(0, num_majors):
            majors.append(json_obj['current_student_majors'][x])

        response['current_student_majors'] = majors

        return response
