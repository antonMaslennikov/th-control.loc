from .ahrefs_analytics import AhrefsAnalytics
import os
import ru_core_news_md

nlp = ru_core_news_md.load()
import pandas as pd


class AnchorsReport:
    def __init__(self):
        self.ahrefs_reports_path = 'AhrefsReports/'

    def project_names(self):
        """
        Функция требуется для подсчета вхождений анкоров по каждому из проектов и формирования
        DataFrame для Pandas.
        :return: Список проектов в словаре.
        """
        projects = {}
        position_project = 0
        for name_project in os.listdir(self.ahrefs_reports_path):
            projects[name_project] = position_project
            position_project += 1
        return projects

    def anchors_list_lemma(self):

        all_projects_anchors = {}
        for name in os.listdir(self.ahrefs_reports_path):
            anchors_qty = {}
            if '.csv' in str(name):
                file_path = self.ahrefs_reports_path + str(name)
                ObjAhrefs = AhrefsAnalytics(file_path)
                data_links = ObjAhrefs.data_links()

                for i in data_links:

                    if not data_links[i]['type_anchor']:  # Проверка на безанкор (True/False)
                        document = nlp(data_links[i]['anchor_text'])  # Формируем список лемм
                        for token in document:

                            if str(token.pos_) != 'NOUN' and \
                                    str(token.pos_) != 'PROPN' and \
                                    str(token.pos_) != 'ADP' and \
                                    str(token.pos_) != 'SYM' and \
                                    str(token.pos_) != 'PUNCT':

                                if anchors_qty.get(name) is None:
                                    anchors_qty[name] = {token.lemma_.lower(): 1}
                                else:
                                    if anchors_qty.get(name).get(token.lemma_.lower()) is None:
                                        anchors_qty[name][token.lemma_.lower()] = 1
                                    else:
                                        anchors_qty[name][token.lemma_.lower()] = int(
                                            anchors_qty[name][token.lemma_.lower()]) + 1
                """
                Собираем финальный список анкоров
                """
                for i in anchors_qty:
                    for word in anchors_qty[i]:

                        qnty_word = anchors_qty[i][word]
                        if all_projects_anchors.get(word) is None:
                            all_projects_anchors[word] = {name: qnty_word}
                        else:
                            all_projects_anchors[word][name] = qnty_word
        return all_projects_anchors

    def dataframe_simple_create(self):
        f = open("res_simple_anchors_report.csv", "w")
        f.truncate()
        f.close()


        position_project = self.project_names()
        dataframe_list = []
        columns_list = ['lemma']

        for project in position_project:
            columns_list.append(project)

        all_projects_anchors = self.anchors_list_lemma()



        for word in all_projects_anchors:
            list_elem = [word]
            for project in position_project:
                if all_projects_anchors[word].get(project) is None:
                    list_elem.append(0)
                else:
                    list_elem.append(all_projects_anchors[word].get(project))
            dataframe_list.append(list_elem)
        res_simple_anchors_report = pd.DataFrame(dataframe_list, columns=columns_list)
        res_simple_anchors_report.to_csv('res_simple_anchors_report.csv', encoding='utf-8-sig')
        return True

    def segment_dr(self, domain_rating):
        try:
            domain_ration = int(domain_rating)
            if domain_rating <= 10:
                return '0-10'
            elif 11 <= domain_rating <= 20:
                return '11-20'
            elif 21 <= domain_rating <= 30:
                return '21-30'
            elif 31 <= domain_rating <= 40:
                return '31-40'
            elif 41 <= domain_rating <= 100:
                return '41-100'
            else:
                return '101+'
        except:
            return "Error"

    def dataframe_detailed_create(self):
        f = open("res_detailed_anchors_report.csv", "w")
        f.truncate()
        f.close()

        columns_list = ['lemma', 'reffering_page_url',
                        'target_url', 'project_name',
                        'type_link', 'nofollow_status',
                        'dr', 'dr_segment', 'qty']

        dataframe_list = []
        for name in os.listdir(self.ahrefs_reports_path):
            if '.csv' in str(name):
                file_path = self.ahrefs_reports_path + str(name)
                ObjAhrefs = AhrefsAnalytics(file_path)
                data_links = ObjAhrefs.data_links()

                for i in data_links:
                    if not data_links[i]['type_anchor']:  # Проверка на безанкор (True/False)
                        document = nlp(data_links[i]['anchor_text'])  # Формируем список лемм
                        for token in document:
                            if str(token.pos_) != 'NOUN' and \
                                    str(token.pos_) != 'PROPN' and \
                                    str(token.pos_) != 'ADP' and \
                                    str(token.pos_) != 'SYM' and \
                                    str(token.pos_) != 'PUNCT':
                                segment_dr = self.segment_dr(data_links[i]['domain_rating'])
                                list_elem = [token.lemma_.lower(), data_links[i]['reffering_page_url'],
                                             data_links[i]['target_url'], name,
                                             data_links[i]['type_link'], data_links[i]['nofollow_status'],
                                             data_links[i]['domain_rating'], segment_dr, 1
                                             ]
                                if list_elem not in dataframe_list:
                                    dataframe_list.append(list_elem)

        res_detailed_anchors_report = pd.DataFrame(dataframe_list, columns=columns_list)
        res_detailed_anchors_report.to_csv('res_detailed_anchors_report.csv', encoding='utf-8-sig')
        return True