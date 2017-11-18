from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class CourseMajors(APIView):

    def get(self, request, section_label, term_id):
        pass
