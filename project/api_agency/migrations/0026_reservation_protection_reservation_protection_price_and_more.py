# Generated by Django 5.0.2 on 2024-06-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0025_branch_is_locked_vehicle_is_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='protection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='protection_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_price_without_protection',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='reservation',
            name='vehicle_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
