# Generated by Django 3.1.4 on 2020-12-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_user_total_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='league_code',
            field=models.CharField(default='none', max_length=10),
            preserve_default=False,
        ),
    ]
