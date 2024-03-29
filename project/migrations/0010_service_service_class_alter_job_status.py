# Generated by Django 4.1.3 on 2023-02-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_remove_job_result_jobresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_class',
            field=models.IntegerField(choices=[(1, 'GoogleIndexer')], null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(choices=[(1, 'Запущен'), (2, 'Успешно завершён'), (3, 'Завершился ошибкой'), (4, 'Промежуточный результат')], default=1),
        ),
    ]
