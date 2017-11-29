from coursedashboards.views.api.course_info import CourseInfoView


class CourseCGPA(CourseInfoView):

    def get_data(self, offering):
        json_obj = {}

        offering.set_json_cumulative_median(json_obj)

        return json_obj


