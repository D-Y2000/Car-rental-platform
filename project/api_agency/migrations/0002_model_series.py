# Generated by Django 4.2 on 2024-02-08 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_agency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='series',
            field=models.CharField(blank=True, help_text='Model', max_length=100, null=True),
        ),
    ]
