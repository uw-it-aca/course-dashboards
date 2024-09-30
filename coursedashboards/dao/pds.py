# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import CharField, OuterRef, Subquery
from django.db.models.functions import JSONObject
from uw_person_client.models import Person, Student, Transcript


def get_students_by_uwnetids(uwnetids):
    return Student.objects.annotate(latest_transcript=Subquery(
            Transcript.objects.filter(
                student=OuterRef('pk')).values(json=JSONObject(
                    scholarship_type='scholarship_type')
                ).order_by('-tran_term__year', '-tran_term__quarter')[:1])
        ).filter(
            person__uwnetid__in=uwnetids
        ).values(
            'person__uwnetid',
            'application_type_code',
            'disability_ind',
            'special_program_code',
            'latest_transcript',
        )


def get_persons_by_uwnetids(uwnetids, **kwargs):
    queryset = Person.objects.filter(uwnetid__in=uwnetids)

    related_fields = Person.objects._include(**kwargs)
    if related_fields:
        queryset.prefetch_related(*related_fields)

    persons = []
    for person in queryset:
        persons.append(Person.objects._assemble(person, **kwargs))

    return persons
