# Generated by Django 3.1.4 on 2020-12-19 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20201218_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='league_model',
        ),
    ]
