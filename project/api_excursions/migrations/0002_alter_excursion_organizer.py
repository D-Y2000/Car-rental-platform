# Generated by Django 5.0.2 on 2024-07-27 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_excursions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursion',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='excursions', to='api_excursions.excursionorganizer'),
        ),
    ]
