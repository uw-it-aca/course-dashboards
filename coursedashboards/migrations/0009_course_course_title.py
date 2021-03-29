# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-26 19:34


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0008_auto_20170926_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_title',
            field=models.CharField(default=b'', max_length=64),
        ),
    ]
