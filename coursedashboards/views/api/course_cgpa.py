from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering
from coursedashboards.views.api.course_info import CourseInfoView


class CourseMedianCGPA(CourseInfoView):

    def get_data(self, offering):
        json_obj = {}

        threads = []
        t = Thread(target=offering.set_json_cumulative_median,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t.join()

        return json_obj


