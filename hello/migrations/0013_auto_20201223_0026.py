# Generated by Django 3.1.4 on 2020-12-23 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0012_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='players',
            field=models.JSONField(default={'CB1': '', 'CB2': '', 'DE1': '', 'DE2': '', 'DT1': '', 'K': '', 'MLB1': '', 'MLB2': '', 'OL1': '', 'OL2': '', 'OL3': '', 'QB': '', 'RB1': '', 'RB2': '', 'S1': '', 'S2': '', 'TE': '', 'W/R': '', 'WR1': '', 'WR2': ''}, max_length=1000),
        ),
    ]
