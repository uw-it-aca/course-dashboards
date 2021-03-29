# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-20 19:16


from django.db import migrations, models

from coursedashboards.models import Term


def reverse_save_term_key(apps, schema_editor):
    pass

def save_term_key(apps, schema_editor):
    terms = Term.objects.all()

    for term in terms:
        term.save()


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0011_auto_20171219_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='term_key',
            field=models.PositiveSmallIntegerField(db_index=True, default=0),
        ),
        migrations.RunPython(save_term_key, reverse_save_term_key)
    ]
