# Generated by Django 4.0.5 on 2023-02-08 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_report_current_date_alter_tasks_assigned_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 629963)),
        ),
        migrations.AlterField(
            model_name='report',
            name='pause_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 629963)),
        ),
        migrations.AlterField(
            model_name='report',
            name='work_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 629963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='assigned_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='finish_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='pause_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='start_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_effective_time',
            field=models.TimeField(default=datetime.datetime(2023, 2, 8, 15, 25, 43, 628963)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_time',
            field=models.TimeField(default=datetime.time(15, 25, 43, 628963)),
        ),
    ]