# Generated by Django 2.2.27 on 2022-03-24 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedashboards', '0015_auto_20210317_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='intro_modal',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]