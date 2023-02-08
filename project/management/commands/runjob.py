from django.core.management.base import BaseCommand
from project.models import Job, ProjectServiceSetting
from services.google_indexing.main import GoogleIndexer


class Command(BaseCommand):
    help = 'Запуск заданий на исполнение'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(status__in=[1, 4]).all()

        for job in jobs:

            if job.service.service_class:

                match job.service.service_class:
                    case 1:
                        Service = GoogleIndexer()

                if Service:

                    print(job.project_id, job.service.name, job.service.service_class)

                    # дёргаем настройки сервиса
                    settings = ProjectServiceSetting.getall(job.project_id, job.service_id)

                    if settings:
                        Service.setSettings(settings)
