import os
from itertools import zip_longest
from .ahrefs_analytics import AhrefsAnalytics
import re
import csv

class CalculateDataSimple():

    def __init__(self, data_links, data_domains):
        self.data_links = data_links
        self.data_domains = data_domains

    def get_links_count(self):
        count_links = len(self.data_links)
        return count_links

    def get_domains_count(self):
        count_domains = len(self.data_domains)
        return count_domains

    def get_type_anchor(self):
        anchors_count = 0
        without_anchors_count = 0
        anchors_count_nofollow = 0
        without_anchors_count_nofollow = 0

        for link in self.data_links:
            if self.data_links[link]['type_anchor']:
                anchors_count += 1
                if self.data_links[link]['nofollow_status'] == 'true':
                    anchors_count_nofollow += 1
            else:
                without_anchors_count += 1
                if self.data_links[link]['nofollow_status'] == 'true':
                    without_anchors_count_nofollow += 1

        return {'anchors_count': anchors_count,
                'without_anchor_count': without_anchors_count,
                'anchors_count_nofollow': anchors_count_nofollow,
                'without_anchors_count_nofollow': without_anchors_count_nofollow
                }

    def get_count_main_or_insite(self):
        count_main_link = 0
        count_main_link_nofollow = 0
        count_other_link = 0
        count_other_link_nofollow = 0
        counter = 0
        for link in self.data_links:
            if counter != 0:
                # print(self.data_links[link])
                link_check = self.data_links[link]['target_url']
                regexp = re.findall(r'\/', link_check)

                if len(regexp) <= 3:
                    count_main_link += 1
                    if self.data_links[link]['nofollow_status'] == 'true':
                        count_main_link_nofollow += 1
                else:
                    count_other_link += 1
                    if self.data_links[link]['nofollow_status'] == 'true':
                        count_other_link_nofollow += 1
                counter += 1
            else:
                counter += 1
        return {'count_main_link': count_main_link,
                'count_other_link': count_other_link,
                'count_main_link_nofollow': count_main_link_nofollow,
                'count_other_link_nofollow': count_other_link_nofollow
                }

    def get_count_traffic_links(self):
        count_links_traffic = 0
        count_links_without_traffic = 0
        for link in self.data_links:
            if self.data_links[link]['page_url_traffic'] >= 1:
                count_links_traffic += 1
            else:
                count_links_without_traffic += 1
        return {'count_links_traffic': count_links_traffic,
                'count_links_without_traffic': count_links_without_traffic
                }

    def get_count_crowd_links(self):
        count_crowd_links = 0
        for link in self.data_links:
            if self.data_links[link]['platform'] == 'message-boards':
                count_crowd_links += 1
        return count_crowd_links

    def mean(self, numbers_list):
        return sum(numbers_list) / len(numbers_list)

    def median(self, numbers_list):
        n = len(numbers_list)
        mid = n // 2
        if n % 2 == 1:
            return sorted(numbers_list)[mid]
        else:
            return self.mean(sorted(numbers_list)[mid - 1:][:2])

    def get_urls_rating(self):
        numbers = []
        for link in self.data_links:
            numbers.append(self.data_links[link]['url_ration'])
        avg_urls_ratings = self.mean(numbers)
        median_urls_ratings = self.median(numbers)
        return {'mean_url_rating': avg_urls_ratings,
                'median_url_rating': median_urls_ratings
                }

    def get_rank_domains(self):
        numbers = []
        for domain in self.data_domains:
            numbers.append(self.data_domains[domain]['dr_domain'])
        avg_domains_ratings = self.mean(numbers)
        median_domains_ratings = self.median(numbers)
        return {'mean_domains_rating': avg_domains_ratings,
                'median_domains_rating': median_domains_ratings
                }

    def get_count_gov_edu_domains_links(self):
        count_gov_edu_domains = 0
        count_gov_edu_links = 0
        for domain in self.data_domains:
            if '.gov' in domain or '.edu' in domain:
                count_gov_edu_domains += 1
        for link in self.data_links:
            if '.gov' in link or '.edu' in link:
                count_gov_edu_links += 1

        return {'count_gov_edu_domains': count_gov_edu_domains,
                'count_gov_edu_links': count_gov_edu_links
                }

    def qty_nofollow_domains(self):
        qty_counter_nofollow_domains = 0
        domains_list = []
        for link in self.data_links:
            if self.data_links[link]['domain_url'] not in domains_list and self.data_links[link]['nofollow_status'] == 'true':
                domains_list.append(self.data_links[link]['domain_url'])
                qty_counter_nofollow_domains += 1
        return qty_counter_nofollow_domains

    def qty_nofollow_links(self):
        qty_counter_nofollow_links = 0
        links_list = []
        for link in self.data_links:
            if link not in links_list and self.data_links[link]['nofollow_status'] == 'true':
                links_list.append(link)
                qty_counter_nofollow_links += 1
        return qty_counter_nofollow_links


    def links_vs_month(self):
        data_month = {}
        avg_cnt_links_month = ''  # Среднее количество обратных ссылок в месяц
        median_cnt_links_month = ''  # Медианное количество обратных ссылок в месяц

        for link in self.data_links:
            """
            Подсчет количества ссылок (общие данные)
            """
            # print(self.data_links[link]['date_trunc'])
            if self.data_links[link]['date_trunc'] != "Error":
                if data_month.get(self.data_links[link]['date_trunc'].date()) is None:
                    data_month[self.data_links[link]['date_trunc'].date()] = {'cnt_links_month': 1,
                                                                              'cnt_links_main_month': 0,
                                                                              'cnt_links_other_month': 0,
                                                                              'cnt_links_main_month_anchors': 0,
                                                                              'cnt_links_main_month_none_anchors': 0,
                                                                              'cnt_links_other_month_anchors': 0,
                                                                              'cnt_links_other_month_none_anchors': 0,
                                                                              }
                else:
                    data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_month'] = \
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_month'] + 1

        for link in self.data_links:
            """
            Подсчет количества ссылок на морду или на внутряки. Сегментация по анкорным и безанкорным.
            """
            if self.data_links[link]['date_trunc'] != "Error":
                link_recheck = self.data_links[link]['target_url']
                regexp = re.findall(r'\/', link_recheck)
                if len(regexp) <= 3:
                    """
                    Ссылки на морду
                    """
                    data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_main_month'] = \
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_main_month'] + 1

                    if self.data_links[link]['type_anchor']:
                        """
                        Анкорные на морду
                        """
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_main_month_anchors'] = \
                            data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_main_month_anchors'] + 1
                    else:
                        """
                        Безанкорные на морду
                        """
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_main_month_none_anchors'] = \
                            data_month[self.data_links[link]['date_trunc'].date()][
                                'cnt_links_main_month_none_anchors'] + 1

                else:
                    """
                    Ссылки на внутряки
                    """
                    data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_other_month'] = \
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_other_month'] + 1

                    if self.data_links[link]['type_anchor']:
                        """
                        Анкорные на внутряк
                        """
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_other_month_anchors'] = \
                            data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_other_month_anchors'] + 1
                    else:
                        """
                        Безанкорные на внутряк
                        """
                        data_month[self.data_links[link]['date_trunc'].date()]['cnt_links_other_month_none_anchors'] = \
                            data_month[self.data_links[link]['date_trunc'].date()][
                                'cnt_links_other_month_none_anchors'] + 1
        sum_cnt_links_main_month = 0
        sum_cnt_links_other_month = 0
        sum_cnt_links_main_month_anchors = 0
        sum_cnt_links_main_month_none_anchors = 0
        sum_cnt_links_other_month_anchors = 0
        sum_cnt_links_other_month_none_anchors = 0
        for i in data_month:
            sum_cnt_links_main_month += data_month[i]['cnt_links_main_month']
            sum_cnt_links_other_month += data_month[i]['cnt_links_other_month']
            sum_cnt_links_main_month_anchors += data_month[i]['cnt_links_main_month_anchors']
            sum_cnt_links_main_month_none_anchors += data_month[i]['cnt_links_main_month_none_anchors']
            sum_cnt_links_other_month_anchors += data_month[i]['cnt_links_other_month_anchors']
            sum_cnt_links_other_month_none_anchors += data_month[i]['cnt_links_other_month_none_anchors']

        avg_sum_cnt_links_main_month = sum_cnt_links_main_month / len(data_month)
        avg_sum_cnt_links_other_month = sum_cnt_links_other_month / len(data_month)
        avg_sum_cnt_links_main_month_anchors = sum_cnt_links_main_month_anchors / len(data_month)
        avg_sum_cnt_links_main_month_none_anchors = sum_cnt_links_main_month_none_anchors / len(data_month)
        avg_sum_cnt_links_other_month_anchors = sum_cnt_links_other_month_anchors / len(data_month)
        avg_sum_cnt_links_other_month_none_anchors = sum_cnt_links_other_month_none_anchors / len(data_month)

        data_month['stat'] = {
            'avg_sum_cnt_links_main_month': avg_sum_cnt_links_main_month,
            'avg_sum_cnt_links_other_month': avg_sum_cnt_links_other_month,
            'avg_sum_cnt_links_main_month_anchors': avg_sum_cnt_links_main_month_anchors,
            'avg_sum_cnt_links_main_month_none_anchors': avg_sum_cnt_links_main_month_none_anchors,
            'avg_sum_cnt_links_other_month_anchors': avg_sum_cnt_links_other_month_anchors,
            'avg_sum_cnt_links_other_month_none_anchors': avg_sum_cnt_links_other_month_none_anchors,
            'cnt_month': len(data_month)
        }
        # print(data_month)
        return data_month

    def prepare_simple_report(self, val_report, name_report):
        anchors_count = self.get_type_anchor()
        count_main_or_other_links = self.get_count_main_or_insite()
        count_traffic_links = self.get_count_traffic_links()
        urls_rating = self.get_urls_rating()
        domains_rating = self.get_rank_domains()
        count_gov_edu_links_domains = self.get_count_gov_edu_domains_links()
        stat_cnt_links = self.links_vs_month()
        qty_nofollow_domains = self.qty_nofollow_domains()
        qty_nofollow_backlinks = self.qty_nofollow_links()

        """
                        'count_main_link_nofollow': count_main_link_nofollow,
                'count_other_link_nofollow': count_other_link_nofollow
        """

        val_report[name_report] = {'Кол-во ссылающихся доменов': self.get_domains_count(),
                                   'Кол-во ссылающихся доменов NOFOLLOW': qty_nofollow_domains,
                                   'Кол-во обратных ссылок': self.get_links_count(),
                                   'Кол-во обратных ссылок NOFOLLOW': qty_nofollow_backlinks,
                                   'Кол-во анкорных ссылок': anchors_count['anchors_count'],
                                   'Кол-во анкорных ссылок NOFOLLOW': anchors_count['anchors_count_nofollow'],
                                   'Кол-во безанкорных ссылок': anchors_count['without_anchor_count'],
                                   'Кол-во безанкорных ссылок NOFOLLOW': anchors_count['without_anchors_count_nofollow'],
                                   'Кол-во ссылок на морду': count_main_or_other_links['count_main_link'],
                                   'Кол-во ссылок на морду NOFOLLOW': count_main_or_other_links['count_main_link_nofollow'],
                                   'Кол-во ссылок на прочие страницы': count_main_or_other_links['count_other_link'],
                                   'Кол-во ссылок на прочие страницы NOFOLLOW': count_main_or_other_links['count_other_link_nofollow'],
                                   'Кол-во ссылок без трафика, шт': count_traffic_links['count_links_without_traffic'],
                                   'Кол-во ссылок с трафиком, шт': count_traffic_links['count_links_traffic'],
                                   'Кол-во крауд ссылок (message-boards)': self.get_count_crowd_links(),
                                   'Медиана URL Rating': round(urls_rating['median_url_rating']),
                                   'Среднее значение URL Rating': round(urls_rating['mean_url_rating']),
                                   'Медиана DR': round(domains_rating['median_domains_rating']),
                                   'Среднее значение DR': round(domains_rating['mean_domains_rating']),
                                   'Количество gov/edu ссылок': count_gov_edu_links_domains['count_gov_edu_links'],
                                   'Количество gov/edu доменов': count_gov_edu_links_domains['count_gov_edu_domains'],
                                   'Среднее кол-во обратных ссылок в месяц на морду': round(
                                       stat_cnt_links['stat']['avg_sum_cnt_links_main_month']),
                                   'Среднее кол-во обратных ссылок в месяц на прочие страницы': round(
                                       stat_cnt_links['stat']['avg_sum_cnt_links_other_month']),
                                   'Среднее кол-во АНКОРНЫХ обратных ссылок в месяц на морду': round(stat_cnt_links['stat'][
                                       'avg_sum_cnt_links_main_month_anchors']),
                                   'Среднее кол-во Б/АНКОРНЫХ обратных ссылок в месяц на морду': round(stat_cnt_links['stat'][
                                       'avg_sum_cnt_links_main_month_none_anchors']),
                                   'Среднее кол-во АНКОРНЫХ обратных ссылок в месяц на прочие страницы':
                                       round(stat_cnt_links['stat']['avg_sum_cnt_links_other_month_anchors']),
                                   'Среднее кол-во Б/АНКОРНЫХ обратных ссылок в месяц на прочие страницы':
                                       round(stat_cnt_links['stat']['avg_sum_cnt_links_other_month_none_anchors']),
                                   'Длительность работы с ссылками, лет': round(stat_cnt_links['stat']['cnt_month'] / 12),
                                   }
        return val_report
        # TODO: Кол-во ссылок на бирже
        # TODO: Кол-во общих ссылок с конкурентами

    def prepare_simple_keys_query_links(self):
        # TODO: Здесь будет подготовка отчета по вхождению ключевых слов в анкоры
        pass


def main():
    simple_report = {}

    crnt_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'

    for name in os.listdir(crnt_dir + 'AhrefsReports'):
        if '.csv' in str(name):
            file_path = crnt_dir + 'AhrefsReports/' + str(name)

            ObjAhrefs = AhrefsAnalytics(file_path)

            data_domains = ObjAhrefs.data_domains()
            data_links = ObjAhrefs.data_links()
            ObjCalculateDataSimple = CalculateDataSimple(data_links=data_links, data_domains=data_domains)
            ObjCalculateDataSimple.prepare_simple_report(val_report=simple_report, name_report=name)

    all_data = []
    file_names = ['Parameters \ Domains']
    row_names = ['Quantity domains pcs', 'Quantity domains NOFOLLOW pcs',
                 'Quantity backlinks pcs', 'Quantity backlinks NOFOLLOW pcs',
                 'Quantity anchor links pcs', 'Quantity anchor links NOFOLLOW pcs',
                 'Quantity without anchor links pcs', 'Quantity without anchor links NOFOLLOW pcs',
                 'Quantity links main page pcs', 'Quantity links NOFOLLOW main page pcs',
                 'Quantity links other pages pcs', 'Quantity links NOFOLLOW other pages pcs',
                 'Quantity links without traffic pcs', 'Quantity links with traffic pcs',
                 'Quantity message boards links pcs',
                 'Median URL Rating', 'AVG URL Rating', 'Median DR',
                 'AVG DR', 'Quantity gov edu links pcs', 'Quantity gov edu domains pcs',
                 'AVG quantity backlinks to MAIN page per MONTH pcs',
                 'AVG quantity backlinks to OTHER pages per MONTH pcs',
                 'AVG quantity anchor backlinks to MAIN page per MONTH pcs',
                 'AVG quantity without anchor backlinks to MAIN page per MONTH pcs',
                 'AVG quantity anchor backlinks to OTHER page per MONTH pcs',
                 'AVG quantity without anchor backlinks to OTHER page per MONTH pcs',
                 'Duration of work with links years'
                 ]

    all_data.append(row_names)
    for i in simple_report:
        column_x = []
        file_names.append(i)
        for a in simple_report[i]:
            column_x.append(simple_report[i][a])
        all_data.append(column_x)

    export_data = zip_longest(*all_data, fillvalue='')

    f = open(crnt_dir + "res_simple_report.csv", "w")
    f.truncate()
    f.close()

    with open(crnt_dir + 'res_simple_report.csv', 'a+', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow((file_names))
        wr.writerows(export_data)
    myfile.close()


if __name__ == '__main__':
    main()
