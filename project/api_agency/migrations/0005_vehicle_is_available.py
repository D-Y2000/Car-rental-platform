# Generated by Django 5.0.2 on 2024-02-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0004_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
