# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-26 17:21


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0007_auto_20170918_2343'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseMedianGPA',
        ),
        migrations.AlterModelOptions(
            name='courseoffering',
            options={'ordering': ['-term__year', '-term__quarter']},
        ),
        migrations.AddField(
            model_name='registration',
            name='credits',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
