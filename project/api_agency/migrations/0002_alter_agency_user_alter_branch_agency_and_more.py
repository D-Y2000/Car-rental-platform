# Generated by Django 5.0.2 on 2024-02-21 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_agency', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='branch',
            name='agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_branches', to='api_agency.agency'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='owned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_cars', to='api_agency.branch'),
        ),
    ]
