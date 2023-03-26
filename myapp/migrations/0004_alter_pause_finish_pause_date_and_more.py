# Generated by Django 4.0.5 on 2023-02-13 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_pause_finish_pause_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pause',
            name='finish_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 299250)),
        ),
        migrations.AlterField(
            model_name='pause',
            name='start_pause_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 299250)),
        ),
        migrations.AlterField(
            model_name='report',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 298250)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 298250)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 298250)),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 13, 15, 22, 31, 298250)),
        ),
    ]
