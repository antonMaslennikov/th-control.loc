import datetime
import os

import httplib2
import json

from oauth2client.service_account import ServiceAccountCredentials
from .script_mysql import MySQLi
from .config import *
from ..Service import Service

"""
pip install google-api-python-client oauth2client
pip install --upgrade oauth2client
"""


class GoogleIndexer(Service):
    json_keys = []

    urls_file = None

    SCOPES = ["https://www.googleapis.com/auth/indexing"]

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

        for json_key in self.json_keys:

            credentials = ServiceAccountCredentials._from_parsed_json_keyfile(json_key, scopes=self.SCOPES)

            http = credentials.authorize(httplib2.Http())

            a_file = open(os.getcwd() + self.urls_file, "r")  # get list of lines
            urls = a_file.readlines()
            a_file.close()

            new_file = open(os.getcwd() + self.urls_file, "w")

            flag = False

            for url in urls:

                url_new = url.rstrip("\n")

                if flag:
                    new_file.write(url)
                else:
                    result = self.indexURL2(url_new, http)

                # print(result)

                if result.get('error'):
                    err = result.get('error')

                    # PERMISSION_DENIED
                    if err['code'] == 403:
                        self.results.append({'url': url_new, 'date': str(datetime.date.today()), 'message': err['message']})
                    else:
                        flag = True
                        new_file.write(url)
                        result = ''
                else:
                    if not flag:
                        self.results.append({'url': url_new, 'date': str(datetime.date.today()), 'message': 'успешно отправлен'})

            # TODO придумать другое условие выхода из цикла по ключам
            # if len(self.results) == len(urls):
            #     break

        new_file.close()

        return self.resultsToString()
