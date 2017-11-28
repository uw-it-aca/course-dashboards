from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from coursedashboards.models import CourseOffering


class CourseSummary(APIView):

    def get(self, request):


        course_offering = CourseOffering()

        summary = self.course_summary(course_offering)

    def course_summary(self, offering):
        json_obj = {}

        threads = []
        t = Thread(target=offering.set_json_cumulative_median,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        t = Thread(target=offering.set_json_current_student_majors,
                   args=(json_obj,))
        threads.append(t)
        t.start()

        past_objs = []

        for co in CourseOffering.objects.filter(
                course=offering.course).select_related('course', 'term'):
            past_obj = {}
            past_objs.append(past_obj)

            t = Thread(target=offering.set_past_course_grades,
                       args=(past_obj,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total = 0.0
        failed = 0.0
        for past_obj in past_objs:
            total += len(past_obj['course_grades'])
            failed += len([grade for grade in past_obj['course_grades']
                          if grade < 2.0])

        fail_rate = failed / total

        response = {}

        response['failure_rate'] = round(fail_rate * 1000) / 10.0
        response['most_common_major'] = json_obj['current_student_majors'][0]
        response['median_cgpa'] = json_obj['current_median']

        return response


