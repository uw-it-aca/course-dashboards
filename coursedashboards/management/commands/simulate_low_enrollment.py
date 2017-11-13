import logging

from django.core.management.base import BaseCommand

from coursedashboards.models import (
    Course, CourseOffering,
    User)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Changes ESS 102 to have an enrollment of 3"

    def handle(self, *args, **options):
        ess_102 = Course.objects.get(curriculum="ESS", course_number=102)
        bill = User.objects.get(uwnetid="bill")
        offerings = CourseOffering.objects.filter(course=ess_102,
                                                  course__instructor__user=bill
                                                  )

        for offering in offerings:
            offering.current_enrollment = 3
            offering.save()

