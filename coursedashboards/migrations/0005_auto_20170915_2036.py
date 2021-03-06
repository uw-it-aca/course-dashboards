# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-15 20:36


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0004_auto_20170907_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcurrentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('concurrent_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Course')),
                ('course_offering', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.CourseOffering')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Course')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Major')),
            ],
        ),
        migrations.CreateModel(
            name='QuarterGPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpa', models.FloatField()),
                ('credits', models.IntegerField()),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.Term')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coursedashboards.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='coursemajor',
            unique_together=set([('major', 'course')]),
        ),
    ]
