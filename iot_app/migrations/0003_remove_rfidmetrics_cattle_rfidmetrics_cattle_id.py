# Generated by Django 5.1.3 on 2024-12-17 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot_app', '0002_rfidmetrics_duration_seconds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfidmetrics',
            name='cattle',
        ),
        migrations.AddField(
            model_name='rfidmetrics',
            name='cattle_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]