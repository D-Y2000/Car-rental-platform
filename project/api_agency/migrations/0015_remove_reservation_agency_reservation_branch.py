# Generated by Django 5.0.2 on 2024-05-06 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0014_rename_rservationnotificatoin_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='agency',
        ),
        migrations.AddField(
            model_name='reservation',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='api_agency.branch'),
        ),
    ]
