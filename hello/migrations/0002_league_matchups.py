# Generated by Django 3.1.4 on 2020-12-29 23:01

from django.db import migrations, models
import hello.models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='matchups',
            field=models.JSONField(default=hello.models.def_json),
        ),
    ]
