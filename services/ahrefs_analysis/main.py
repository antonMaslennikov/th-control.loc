import json
import os

from ..Service import Service

import datetime
import shutil

from .libs.anchors_report import AnchorsReport
from .libs.simple_report import SimpleReport

class AhrefsAnalysis(Service):

    files = []

    def setSettings(self, settings):
        pass

    def setData(self, files):
        self.files = json.loads(files)

    def run(self):
        print(f"Запущено формирование файла: res_simple_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")

        ObjSimpleReport = SimpleReport(self.files)
        res1 = ObjSimpleReport.create()

        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n")

        self.Job.appendResults([{'simple_report': res1,
                             'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                             'message': 'успешно создан'}])

        # ---------------------------------------------------------------------

        print(f"Запущено формирование файла: res_simple_anchors_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")

        ObjAnchorsReport = AnchorsReport(self.files)
        res2 = ObjAnchorsReport.dataframe_simple_create()

        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n")

        self.Job.appendResults([{'simple_anchors_report': res2,
                             'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                             'message': 'успешно создан'}])

        # ---------------------------------------------------------------------

        print(f"Запущено формирование файла: res_detailed_anchors_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")

        ObjAnchorsReport = AnchorsReport(self.files)
        res3 = ObjAnchorsReport.dataframe_detailed_create()

        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n")

        self.Job.appendResults([{'detailed_anchors_report': res3,
                             'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                             'message': 'успешно создан'}])

        # ---------------------------------------------------------------------

        self.full_complite = True

        return self.results.append({
            'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
            'message': 'полностью завершено'}
        )
