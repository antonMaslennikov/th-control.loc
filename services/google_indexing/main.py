import datetime
import os

import httplib2
import json

from oauth2client.service_account import ServiceAccountCredentials
from ..Service import Service

"""
pip install google-api-python-client oauth2client
pip install --upgrade oauth2client
"""


class GoogleIndexer(Service):
    json_keys = []

    urls_file = None

    SCOPES = ["https://www.googleapis.com/auth/indexing"]

    standart_dalay = 24

    def setSettings(self, settings):

        if not settings['keys']:
            raise 'Не заданы ключи'

        keys = settings['keys']

        while keys.find('}') > 0:
            index = keys.find('}') + 1
            self.json_keys.append(json.loads(keys[0:index].strip()))
            keys = keys[index:]

        if len(self.json_keys) == 0:
            raise 'Не удалось получить ключи'

    def setData(self, file):

        self.urls_file = file

        pass

    def indexURL2(self, u, http):
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        content = {'url': u.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
        result = json.loads(content.decode())

        return result
        # For debug purpose only
        # if "error" in result:
        #     print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
        #                                       result["error"]["message"]))
        #     return "Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"],
        #                                        result["error"]["message"])
        # else:
        #     print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
        #     print("urlNotificationMetadata.latestUpdate.url: {}".format(
        #         result["urlNotificationMetadata"]["latestUpdate"]["url"]))
        #     print("urlNotificationMetadata.latestUpdate.type: {}".format(
        #         result["urlNotificationMetadata"]["latestUpdate"]["type"]))
        #     print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(
        #         result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
        #     return "OK"

    def resultsToString(self):

        str = ''

        for r in self.results:
            str += r.get('date') + ": " + r.get('url') + " (" + r.get('message') + ")\n"

        return str

    def run(self):

        # кол-во корректно обработанных урлов
        processed = 0

        a_file = open(os.getcwd() + self.urls_file, "r")
        urls = a_file.readlines()
        # общее изначальное кол-во урлов на обработке
        total_urls = len(urls)

        for json_key in self.json_keys:

            credentials = ServiceAccountCredentials._from_parsed_json_keyfile(json_key, scopes=self.SCOPES)

            http = credentials.authorize(httplib2.Http())

            a_file = open(os.getcwd() + self.urls_file, "r")
            urls = a_file.readlines()
            a_file.close()

            new_file = open(os.getcwd() + self.urls_file, "w")

            flag = False

            for url in urls:

                print(url)

                if flag:
                    # если на предыдущем шаге произошла ошибка, то скидываем все оставшиеся урлы в файл
                    # и переходим к следующему ключу
                    new_file.write(url)
                    continue
                else:
                    result = self.indexURL2(url.rstrip("\n"), http)

                print(result)

                if result.get('error'):
                    err = result.get('error')

                    # PERMISSION_DENIED
                    if err['code'] == 403 or err['code'] == 301:
                        self.results.append({'url': url, 'date': str(datetime.date.today()), 'message': err['message']})
                        processed += 1
                    # ошибку не удалось определить и выполнение сервиса приостанавливается
                    # в основном ловим (err['code'] == 429 Quota exceeded)
                    else:
                        flag = True
                        new_file.write(url)
                else:
                    self.results.append({'url': url, 'date': str(datetime.date.today()), 'message': 'успешно отправлен'})
                    processed += 1

        new_file.close()

        if processed == total_urls:
            self.full_complite = True
        else:
            self.intermediate_complite = True
            self.last_error = err['message']

        return self.resultsToString()
