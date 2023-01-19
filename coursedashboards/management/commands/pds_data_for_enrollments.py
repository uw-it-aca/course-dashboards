# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from uw_person_client.clients.core_client import UWPersonClient
from coursedashboards.models import Course, CourseOffering, Term
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "dump a field from pds for each regisration in given course"

    def add_arguments(self, parser):
        parser.add_argument('course', type=str)
        parser.add_argument('field', type=str)

    def handle(self, *args, **options):
        year, quarter, curriculum, number, section = tuple(
            options['course'].split('-'))
        fields = options['field'].split('.')

        term = Term.objects.get(quarter=quarter, year=int(year))
        course = Course.objects.get(
            curriculum=curriculum, course_number=int(number),
            section_id=section)
        offering = CourseOffering.objects.get(term=term, course=course)
        regs = offering.get_registrations()
        client = UWPersonClient()
        for r in regs:
            netid = r.user.uwnetid
            p = client.get_person_by_uwnetid(netid)
            v = None
            for f in fields:
                try:
                    if not v:
                        v = getattr(p, f)
                    elif isinstance(v, list):
                        v2 = []
                        for x in v:
                            v2.append(getattr(x, f))
                        v = v2
                    else:
                        v = getattr(v, f)
                except AttributeError:
                    break

            print("{}: {}: {}".format(options['field'], netid, v))
