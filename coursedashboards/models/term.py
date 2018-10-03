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

    def __eq__(self, other):
        return (other is not None and
                type(self) == type(other) and
                self.int_key() == other.int_key())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return (type(self) == type(other) and
                self.int_key() < other.int_key())

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return (type(self) == type(other) and
                self.int_key() > other.int_key())

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    @staticmethod
    def _quarter_to_int(quarter):
        if quarter.lower() == Term.WINTER:
            return 1
        if quarter.lower() == Term.SPRING:
            return 2
        if quarter.lower() == Term.SUMMER:
            return 3
        return 4

    def int_key(self):
        return int(self.year) * 10 + self._quarter_to_int(self.quarter)
