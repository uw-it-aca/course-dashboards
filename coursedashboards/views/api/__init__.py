from django.http import HttpResponse
from rest_framework.authentication import RemoteUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from coursedashboards.models import Term, Course, CourseOffering
from coursedashboards.views.error import _make_response, MYUW_DATA_ERROR


class CoDaAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def get_offering(self, year, quarter, curriculum, course_number,
                     section_id):
        term = Term.objects.get(year=year, quarter=quarter.lower())
        course = Course.objects.get(curriculum=curriculum.upper(),
                                    course_number=course_number,
                                    section_id=section_id.upper())
        offering = CourseOffering.objects.get(term=term, course=course)
        return offering

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
