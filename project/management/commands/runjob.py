from django.core.management.base import BaseCommand
from project.models import Job, ProjectServiceSetting, JobResult
from services.google_indexing.main import GoogleIndexer


class Command(BaseCommand):
    help = 'Запуск заданий на исполнение'

    def handle(self, *args, **options):

        # TODO добавить проверку на запуск не более 3х раз
        # TODO задания со статусом 4 можно перезапускать только через день после прошлого запуска

        jobs = Job.objects.filter(
            status__in=[0, 4]
        ).order_by('id')[:1]

        for job in jobs:

            job.start()

            if job.service.service_class:

                match job.service.service_class:
                    case 1:
                        Service = GoogleIndexer()

                if Service:

                    print(job.id, ': ', job.data, job.project_id, job.service.name, job.service.service_class)

                    # дёргаем настройки сервиса
                    settings = ProjectServiceSetting.getall(job.project_id, job.service_id)

                    if settings:
                        Service.setSettings(settings)

                    # дёргаем данные для обработки
                    if job.data:
                        Service.setData(job.data)

                    # запускаем сервис
                    results = Service.run()

                    # пишем результаты в логи
                    R = JobResult()
                    R.job_id = job.id
                    R.result = results
                    R.save()

                    # сервис отработал, но не полностью, задание требует повторного запуска
                    if Service.intermediate_complite:
                        job.intermediate()
                    else:
                        #  сервис отработал полностью и может задание может быть завершено
                        if Service.full_complite:
                            job.finish()

                else:
                    job.error('Не обнаружен скрипт сервиса')
            else:
                job.error('Не задан скрипт сервиса')