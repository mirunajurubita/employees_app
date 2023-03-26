# Generated by Django 4.0.5 on 2023-02-08 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_tasks_finish_pause_date_tasks_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='active_tasks',
        ),
        migrations.RemoveField(
            model_name='report',
            name='pause_hours',
        ),
        migrations.RemoveField(
            model_name='report',
            name='pause_minutes',
        ),
        migrations.RemoveField(
            model_name='report',
            name='working_hours',
        ),
        migrations.RemoveField(
            model_name='report',
            name='working_minutes',
        ),
        migrations.AddField(
            model_name='report',
            name='pause_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AddField(
            model_name='report',
            name='tasks',
            field=models.ManyToManyField(to='myapp.tasks'),
        ),
        migrations.AddField(
            model_name='report',
            name='work_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='report',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='finish_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='pause_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='start_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_effective_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 10, 1, 39, 34204)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_time',
            field=models.TimeField(default=datetime.time(10, 1, 39, 34204)),
        ),
    ]