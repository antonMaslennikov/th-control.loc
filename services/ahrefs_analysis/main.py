from ..Service import Service

import datetime

from .libs.anchors_report import AnchorsReport
from .libs.simple_report import main

class AhrefsAnalysis(Service):

    def setSettings(self, settings):
        pass
    def setData(self, files):
        pass

    def run(self):
        print(f"Запущено формирование файла: res_simple_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")
        main()  # res_simple_report.csv
        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n"
              f"Запущено формирование файла: res_simple_anchors_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")
        ObjAnchorsReport = AnchorsReport()
        ObjAnchorsReport.dataframe_simple_create()  # res_simple_anchors_report.csv
        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n")
        print(f"Запущено формирование файла: res_detailed_anchors_report.csv\n"
              f"Время старта: {datetime.datetime.now()}")
        ObjAnchorsReport = AnchorsReport()
        ObjAnchorsReport.dataframe_detailed_create()  # res_simple_anchors_report.csv
        print(f"Формирование файла завершено."
              f"Время окончания: {datetime.datetime.now()}\n")