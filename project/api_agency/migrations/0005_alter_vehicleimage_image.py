# Generated by Django 5.0.2 on 2024-03-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0004_alter_vehicleimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.ImageField(upload_to='imges/vehicles/1'),
        ),
    ]
