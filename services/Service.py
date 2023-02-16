
class Service:

    # сервис отработал полностью и может быть закрыт
    full_complite = False

    # сервис отработал частично и требует повторного запуска
    intermediate_complite = False

    # стандартный интервал в часах для повторного запуска сервиса
    standart_dalay = 1

    results = []

    last_error = None

    def setSettings(self, settings):
        pass

    def setData(self, data):
        pass

    def resultsToString(self):
        pass