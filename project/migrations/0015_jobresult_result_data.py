# Generated by Django 4.1.5 on 2023-02-23 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_job_delayed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobresult',
            name='result_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
