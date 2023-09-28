from django.core.management import BaseCommand

from services.looker_studio.lib.sync_plan_pbn import clear_and_save_data


class Command(BaseCommand):
    help = 'Обновление данныйх из таблицы в базу данных для таблицы pbn_plans'

    def handle(self, *args, **options):
        clear_and_save_data()
        pass