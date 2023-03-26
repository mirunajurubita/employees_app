# Generated by Django 4.0.5 on 2023-02-08 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_report_current_date_alter_report_pause_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 14, 55, 12, 311843)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 14, 55, 12, 307844)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 14, 55, 12, 307844)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='finish_pause_date',
            field=models.DateTimeField(default=datetime.time(14, 55, 12, 308845)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='pause_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='start_pause_date',
            field=models.DateTimeField(default=datetime.time(14, 55, 12, 308845)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 8, 14, 55, 12, 307844)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_effective_time',
            field=models.TimeField(default=datetime.time(14, 55, 12, 308845)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]