# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-18 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0005_auto_20170915_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOfferingMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'CourseOfferingMajor',
            },
        ),
        migrations.AlterUniqueTogether(
            name='coursemajor',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='coursemajor',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursemajor',
            name='major',
        ),
        migrations.AlterField(
            model_name='course',
            name='curriculum',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='CourseMajor',
        ),
        migrations.AddField(
            model_name='courseofferingmajor',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Course'),
        ),
        migrations.AddField(
            model_name='courseofferingmajor',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Major'),
        ),
        migrations.AddField(
            model_name='courseofferingmajor',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Term'),
        ),
        migrations.AlterUniqueTogether(
            name='courseofferingmajor',
            unique_together=set([('major', 'term', 'course')]),
        ),
    ]
