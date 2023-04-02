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
        self.files = files
        pass

    def run(self):
        print(f"Запущено формирование файла: res_simple_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")

        ObjSimpleReport = SimpleReport([self.files])
        res = ObjSimpleReport.create()

        self.results.append({'simple_report': res,
                             'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                             'message': 'успешно создан'})

        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n"
              f"Запущено формирование файла: res_simple_anchors_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")

        # ObjAnchorsReport = AnchorsReport()
        # ObjAnchorsReport.dataframe_simple_create()  # res_simple_anchors_report.csv
        # print(f"Формирование файла завершено."
        #       f"Время окончания: {datetime.datetime.now()}\n")
        # print(f"Запущено формирование файла: res_detailed_anchors_report.csv\n"
        #       f"Время старта: {datetime.datetime.now()}")
        # ObjAnchorsReport = AnchorsReport()
        # ObjAnchorsReport.dataframe_detailed_create()  # res_simple_anchors_report.csv
        # print(f"Формирование файла завершено."
        #       f"Время окончания: {datetime.datetime.now()}\n")

        self.full_complite = True

        return self.results