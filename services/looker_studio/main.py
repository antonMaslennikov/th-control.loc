import datetime
import os
import json

from ..Service import Service
from lookerdb import LookerDb

class LookerStudio(Service):
    standart_dalay = 24

    def setSettings(self, settings):

        if not settings['connection_setting']:
            raise 'Не заданы настройки баз данных'

        for key in settings['connection_setting']:
            self.json_keys.append(json.loads(key.strip()))

        if len(self.json_keys) == 0:
            raise 'Не удалось получить настройки баз данных'

    def setData(self, file):
        self.urls_file = file


    def run(self):

        return self.results
