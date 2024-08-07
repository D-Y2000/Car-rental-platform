# Generated by Django 5.0.2 on 2024-07-14 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_destination', '0002_rename_rate_destinationrate_destinationfeedback'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destinations', to=settings.AUTH_USER_MODEL),
        ),
    ]
