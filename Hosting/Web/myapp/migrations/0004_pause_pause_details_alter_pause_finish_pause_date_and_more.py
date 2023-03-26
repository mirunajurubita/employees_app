# Generated by Django 4.0.5 on 2023-02-07 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_pause_pause_time_alter_pause_finish_pause_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pause',
            name='pause_details',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='pause',
            name='finish_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 960280)),
        ),
        migrations.AlterField(
            model_name='pause',
            name='pause_time',
            field=models.TimeField(default=datetime.time(11, 15, 37, 960280)),
        ),
        migrations.AlterField(
            model_name='pause',
            name='start_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 960280)),
        ),
        migrations.AlterField(
            model_name='report',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 959280)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 959280)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 959280)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 11, 15, 37, 959280)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_time',
            field=models.TimeField(default=datetime.time(11, 15, 37, 959280)),
        ),
    ]
