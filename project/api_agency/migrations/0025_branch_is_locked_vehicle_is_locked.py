# Generated by Django 5.0.2 on 2024-05-30 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0024_wilaya_clicks_count_locationimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
