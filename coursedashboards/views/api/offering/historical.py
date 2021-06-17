from coursedashboards.views.api.endpoint import CoDaEndpoint
from coursedashboards.dao.user import get_current_user


class HistoricalCourseData(CoDaEndpoint):

    def get_data(self, offering):
        instructor = get_current_user().uwnetid if (
            self.request.GET.get('instructed', '') in [
                '1', 'true']) else None

        return offering.past_offerings_json_object(
            past_year=self.request.GET.get('past_year', ''),
            past_quarter=self.request.GET.get('past_quarter', ''),
            instructor=instructor)
