import csv
from urllib.parse import urlparse
from datetime import datetime


class AhrefsAnalytics:
    def __init__(self, file_path):
        self.file_path = file_path
        pass

    def valid_number_int(self, row_valid):
        try:
            self.row_valid = int(row_valid)
            if isinstance(self.row_valid, int):
                return int(self.row_valid)
            else:
                return 0
        except:
            return 0

    def valid_number_float(self, row_valid):
        try:
            self.row_valid = row_valid
            return float(self.row_valid)
        except:
            return 0

    def valid_domain(self, row_valid):
        try:
            self.row_valid = row_valid
            domain = urlparse(self.row_valid).netloc
            if domain:
                return domain
            else:
                return "Error"
        except:
            return "Error"

    def valid_link(self, row_valid):
        try:
            self.row_valid = row_valid
            pass
        except:
            pass

    def valid_text(self, row_valid):
        try:
            self.row_valid = row_valid
            pass
        except:
            pass

    def valid_date(self, row_valid):
        try:
            self.row_valid = row_valid
            datetime_str = self.row_valid
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return datetime_object
        except Exception as e:
            # print("Error datetime object:", str(e))
            return None

    def get_type_anchor_simple(self, anchor_text):
        try:
            domain = urlparse(anchor_text).netloc
            if domain:
                return True  # Безанкорная ссылка
            else:
                return False
        except:
            return False

    def get_type_anchor_hard(self, anchor_text):
        try:
            if self.get_type_anchor_simple(anchor_text):
                return True
            else:
                # TODO: Сюда вставить функцию, определяющую тип анкора. Написать в отдельном файле. Взять с майки
                False
        except:
            return False

    def read_file(self):
        # print(self.file_path)
        file = open(self.file_path, encoding='utf-8')
        csvreader = csv.reader(file)
        return csvreader

    def data_links(self):
        csv_data = self.read_file()
        data_links = {}
        for row in csv_data:

            reffering_page_title = row[0]
            reffering_page_url = row[1]

            domain_url = self.valid_domain(reffering_page_url)

            language = row[2]
            platform = row[3]

            domain_rating = row[5]
            domain_rating = self.valid_number_int(domain_rating)

            url_rating = row[6]
            url_rating = self.valid_number_float(url_rating)

            reffering_domains = row[8]
            linked_domains = row[9]
            external_links = row[10]

            page_traffic = row[11]
            page_traffic = self.valid_number_int(page_traffic)

            keywords = row[12]
            keywords = self.valid_number_int(keywords)

            target_url = row[13]
            left_content = row[14]

            anchor_text = row[15]
            type_anchor = self.get_type_anchor_simple(anchor_text)

            right_content = row[16]
            type_link = row[17]
            nofollow_status = row[19]

            first_seen = row[27]
            first_seen = self.valid_date(first_seen)
            if first_seen is not None:
                date_trunc = first_seen.replace(day=1)
            else:
                date_trunc = "Error"
            if data_links.get(reffering_page_url) is None:
                data_links[reffering_page_url] = {
                    'reffering_page_url': reffering_page_url,
                    'reffering_page_title': reffering_page_title,
                    'language': language,
                    'platform': platform,
                    'url_ration': url_rating,
                    'reffering_domains': reffering_domains,
                    'linked_domains': linked_domains,
                    'external_links': external_links,
                    'page_url_traffic': page_traffic,
                    'keywords_count': keywords,
                    'target_url': target_url,
                    'left_content': left_content,
                    'anchor_text': anchor_text,
                    'type_anchor': type_anchor,
                    'right_content': right_content,
                    'type_link': type_link,
                    'nofollow_status': nofollow_status,
                    'first_seen': first_seen,
                    'date_trunc': date_trunc,
                    'domain_rating': domain_rating,
                    'domain_url': domain_url
                }
        return data_links

    def data_domains(self):
        csv_data = self.read_file()
        data_domains = {}
        cnt_row = 0
        for row in csv_data:
            if cnt_row != 0:
                reffering_page_url = row[1]
                domain = self.valid_domain(reffering_page_url)

                domain_rating = row[5]
                domain_rating = self.valid_number_int(domain_rating)

                domain_traffic = row[7]
                domain_traffic = self.valid_number_int(domain_traffic)

                if data_domains.get(domain) is None:
                    data_domains[domain] = {'dr_domain': domain_rating,
                                            'traffic_domain': domain_traffic,
                                            'links_cnt': 1
                                            }
                else:
                    data_domains[domain]['links_cnt'] = data_domains[domain]['links_cnt'] + 1
            cnt_row += 1
        return data_domains
