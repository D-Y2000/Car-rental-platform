# Generated by Django 5.0.2 on 2024-04-30 13:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0013_rservationnotificatoin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RservationNotificatoin',
            new_name='Notification',
        ),
    ]
