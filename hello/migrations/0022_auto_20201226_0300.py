# Generated by Django 3.1.4 on 2020-12-26 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0021_league_draft_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='draft_started_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
