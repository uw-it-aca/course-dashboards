# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 16:29


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMedianGPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.CharField(db_index=True, max_length=100, unique=True)),
                ('date_saved', models.DateTimeField()),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uwnetid', models.SlugField(max_length=16, unique=True)),
                ('uwregid', models.CharField(db_index=True, max_length=32, null=True, unique=True)),
                ('last_visit', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
