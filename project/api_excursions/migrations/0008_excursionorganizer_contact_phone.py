# Generated by Django 5.0.2 on 2024-08-06 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_excursions', '0007_excursion_places_alter_excursion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursionorganizer',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
