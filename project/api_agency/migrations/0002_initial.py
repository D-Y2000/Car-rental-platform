# Generated by Django 5.0.2 on 2024-03-06 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_agency', '0001_initial'),
        ('api_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_main.profile'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.energy'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='make',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.make'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.model'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='options',
            field=models.ManyToManyField(blank=True, to='api_agency.option'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='owned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_vehicles', to='api_agency.branch'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='transmission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.transmission'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.type'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_agency.vehicle'),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api_agency.vehicle'),
        ),
    ]
