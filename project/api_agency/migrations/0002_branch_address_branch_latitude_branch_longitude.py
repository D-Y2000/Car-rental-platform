# Generated by Django 5.0.2 on 2024-04-21 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='branch',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]