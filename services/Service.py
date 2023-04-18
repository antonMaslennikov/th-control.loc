import json

class Service:

    # сервис отработал полностью и может быть закрыт
    full_complite = False

    # сервис отработал частично и требует повторного запуска
    intermediate_complite = False

    # стандартный интервал в часах для повторного запуска сервиса
    standart_dalay = 1

    results = []

    last_error = None

    Job = None

    def setSettings(self, settings):
        pass

    def setData(self, data):
        pass

    def setJob(self, Job):
        self.Job = Job

    def resultsToString(self):
        pass

    def resultsToJson(self):
        return json.dumps(self.results, ensure_ascii=False)
