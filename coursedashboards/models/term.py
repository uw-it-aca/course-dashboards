from django.utils import timezone
from django.db import models


class Term(models.Model):
    SPRING = 'spring'
    SUMMER = 'summer'
    AUTUMN = 'autumn'
    WINTER = 'winter'

    QUARTERNAME_CHOICES = (
        (WINTER, 'Winter'),
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (AUTUMN, 'Autumn'),
    )

    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    year = models.PositiveSmallIntegerField()

    last_queried = models.DateTimeField(null=True, blank=True)
    term_key = models.PositiveSmallIntegerField(db_index=True, default=0)

    def __str__(self):
        return "%s-%s" % (self.year, self.quarter)

    def get_term_key(self):
        return self.year * 10 + self._quarter_to_int(self.quarter)

    def save(self, *args, **kwargs):
        if self.term_key is 0:
            self.term_key = self.get_term_key()

        super(Term, self).save(*args, **kwargs)

    @staticmethod
    def compare_terms(first, other):
        if first.year < other.year:
            return -1
        elif other.year < first.year:
            return 1

        if (Term._quarter_to_int(first.quarter) <
                Term._quarter_to_int(other.quarter)):
            return -1

        return 1

    @staticmethod
    def _quarter_to_int(quarter):
        if quarter.lower() == Term.WINTER:
            return 1
        elif quarter.lower() == Term.SPRING:
            return 2
        elif quarter.lower() == Term.SUMMER:
            return 3
        elif quarter.lower() == Term.AUTUMN:
            return 4

    def __eq__(self, other):
        return (other is not None and
                type(self) == type(other) and
                self.year == other.year and
                self.quarter == other.quarter)
