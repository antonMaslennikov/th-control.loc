# Generated by Django 4.1.3 on 2023-02-28 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_jobresult_result_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobresult',
            name='result_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
