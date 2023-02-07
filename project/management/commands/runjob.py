from django.core.management.base import BaseCommand
from project.models import Job

class Command(BaseCommand):
    help = 'Запуск заданий на исполнение'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(status__in=[1, 4]).all()

        for job in jobs:
            print(job.project_id, job.service_id, job.status)