# Generated by Django 5.0.2 on 2024-04-27 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0008_vehicle_is_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wilaya',
            options={'ordering': ['code']},
        ),
    ]