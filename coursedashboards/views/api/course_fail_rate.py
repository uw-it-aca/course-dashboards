from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering
from coursedashboards.views.api.course_info import CourseInfoView


class CourseFailRate(CourseInfoView):

    def get_data(self, offering):

        response = {}

        offering.set_fail_rate(response)

        return response


