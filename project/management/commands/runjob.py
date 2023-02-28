import os
import time

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from project.models import Job, ProjectServiceSetting, JobResult
from services.google_indexing.main import GoogleIndexer
from django.db import connection



class Command(BaseCommand):
    help = 'Запуск заданий на исполнение'

    def handle(self, *args, **options):

        # выбираем задачи со статусом 0 или 4
        # запускались не более 10х раз
        # задания со статусом 4 можно перезапускать только через после истечения таймаута

        jobs = Job.objects.filter(
            Q(status=0) | Q(status=4, delayed_at__lt=timezone.now()),
            repeats__lt=10
        ).order_by('id')[:1]

        for job in jobs:

            job.start()

            if job.service.service_class:

                print(job.id, ': ', job.data, job.project_id, job.service.name, job.service.service_class)

                if job.service.service_class == 1:
                    Service = GoogleIndexer()

                if Service:

                    print('run job')

                    job.repeats += 1
                    job.last_repeat = timezone.now()
                    job.save()

                    # дёргаем настройки сервиса
                    try:
                        settings = ProjectServiceSetting.getall(job.project_id, job.service_id)

                        if settings:
                            Service.setSettings(settings)

                        # дёргаем данные для обработки
                        if job.data:
                            Service.setData(job.data)

                        # запускаем сервис
                        Service.run()
                        # time.sleep(120)

                        # за время работы сервиса, джанго гарантированно теряет коннект с базой, переконекчиваемся
                        connection.connection.close()
                        connection.connection = None

                        # пишем результаты в логи
                        R = JobResult()
                        R.job_id = job.id
                        R.result = Service.resultsToString()
                        R.result_data = Service.resultsToJson()
                        R.save()

                        # сервис отработал, но не полностью, задание требует повторного запуска
                        if Service.intermediate_complite:
                            job.intermediate(message=Service.last_error)
                        else:
                            #  сервис отработал полностью и может задание может быть завершено
                            if Service.full_complite:
                                job.finish()

                    except Exception as e:
                        job.error(str(e))
                else:
                    job.error('Не обнаружен скрипт сервиса')
            else:
                job.error('Не задан скрипт сервиса')