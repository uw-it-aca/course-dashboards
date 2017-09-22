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

    def __str__(self):
        return "%s,%s" % (self.year, self.quarter)
