# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-25 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0009_course_course_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='degree_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='is_alum',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='major',
            name='major',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]
