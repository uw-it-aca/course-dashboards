# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-05 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0002_auto_20170831_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_repeat',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
