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

        for key in settings['keys']:
            self.json_keys.append(json.loads(key.strip()))

        if len(self.json_keys) == 0:
            raise 'Не удалось получить ключи'

    def setData(self, file):
        self.urls_file = file

    def indexURL(self, u, http):

        print(len(u.strip()))

        if len(u.strip()) == 0:
            return {}

        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        content = {'url': u.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
        result = json.loads(content.decode())

        return result

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

            a_file = open(os.getcwd() + self.urls_file, "r", encoding="utf-8")
            urls = a_file.readlines()
            a_file.close()

            new_file = open(os.getcwd() + self.urls_file, "w", encoding="utf-8")

            for i, url in enumerate(urls):

                print(i, url)

                result = self.indexURL(url[url.find('http'):].rstrip("\n"), http)

                if result.get('error'):
                    err = result.get('error')

                    # PERMISSION_DENIED
                    if err['code'] == 403 or err['code'] == 301:
                        self.results.append({'url': url, 'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')), 'message': err['message']})
                        processed += 1
                    # Unknown Error
                    elif err['code'] == 500:
                        new_file.writeline(url)
                        self.results.append(
                            {'url': url, 'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                             'message': err['message']})
                    else:
                        # ошибку не удалось определить и выполнение сервиса приостанавливается
                        # в основном ловим (err['code'] == 429 Quota exceeded)
                        # сбрасываем в файл все оставшиеся необработанные урлы
                        new_file.writelines(urls[i:])
                        break
                else:
                    self.results.append({'url': url, 'date': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')), 'message': 'успешно отправлен'})
                    processed += 1

        new_file.close()

        if processed == total_urls:
            self.full_complite = True
        else:
            self.intermediate_complite = True
            self.last_error = err['message']

        return self.results
