# Generated by Django 4.1.5 on 2023-03-11 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_alter_jobresult_result_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectservicesetting',
            unique_together=set(),
        ),
    ]
