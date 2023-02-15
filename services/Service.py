
class Service:

    # сервис отработал полностью и может быть закрыт
    full_complite = False

    # сервис отработал частично и требует повторного запуска
    intermediate_complite = False

    results = []

    def setSettings(self, settings):
        pass

    def setData(self, data):
        pass

    def resultsToString(self):
        pass