from django.core.management.base import BaseCommand
from datetime import datetime
from coursedashboards.models import Term


class Command(BaseCommand):
    help = "Populate user, major, course, instructor tables for specified term"

    def add_arguments(self, parser):
        parser.add_argument('quarter')
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        # determine change_since
        #   if none, one year back from start of term should do
        try:
            term = Term.objects.get(quarter=options['quarter'],
                                    year=options['year'])
            change_since = term.last_queried
        except Term.DoesNotExist:
            term = Term(quarter=options['quarter'],
                        year=options['year'])
            term.save()

        # fetch all courses for the term, changed since the date
            # fill in course details
            # fill in instructor details
            # fetch canvas url based on sis_id
            # fetch course registrations
                # fill in all the user and registration details

        # remember the last time we crawled this term
        term.last_queried = datetime.now()
        term.save()
