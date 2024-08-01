# Generated by Django 5.0.2 on 2024-08-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_excursions', '0005_alter_excursionorganizer_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
