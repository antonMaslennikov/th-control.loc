import datetime
import os

from ..Service import Service
from lookerdb import LookerDb


class LookerStudio(Service):
    standart_dalay = 24
    api_key = None
    def setSettings(self, settings):

        if not settings['api_key']:
            raise 'Не задан ключ по умолчания для всех пбн сайтов'

        for key in settings['api_key']:
            self.api_key = key.strip()

        if len(self.api_key) == 0:
            raise 'Не удалось получить ключ апи'

    def setData(self, file):
        self.urls_file = file

    def run(self):

        return self.results
