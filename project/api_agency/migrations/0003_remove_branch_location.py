# Generated by Django 5.0.2 on 2024-04-21 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0002_branch_address_branch_latitude_branch_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='location',
        ),
    ]