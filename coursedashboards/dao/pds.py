# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.models import Person
from uw_person_client.exceptions import PersonNotFoundException


def get_persons_by_uwnetids(uwnetids, **kwargs):
    queryset = Person.objects.filter(uwnetid__in=uwnetids)

    related_fields = Person.objects._include(**kwargs)
    if related_fields:
        queryset.prefetch_related(*related_fields)

    persons = []
    for person in queryset:
        persons.append(Person.objects._assemble(person, **kwargs))

    return persons
