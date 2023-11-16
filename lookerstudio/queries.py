from django.core.paginator import Paginator
from django.db import connections, connection

from thcontrol.settings import LOOKER_DB_KEY


def execute_select_query(query, params=None, fetch_single=False):
    with connections[LOOKER_DB_KEY].cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        if fetch_single:
            result = cursor.fetchone()
            json_results = dict(zip(columns, result))
        else:
            result = cursor.fetchall()
            json_results = [dict(zip(columns, row)) for row in result]

    return json_results


def execute_update_insert_query(query, params=None):
    with connections[LOOKER_DB_KEY].cursor() as cursor:
        cursor.execute(query, params)
        affected_rows = cursor.rowcount
    return affected_rows


def get_query_result(query, params=None):
    with connections[LOOKER_DB_KEY].cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
    return results


def get_paginator(sql_query, params, current_page=1, items_per_page=20):
    results = execute_select_query(sql_query, params)
    paginator = Paginator(results, items_per_page)
    page = paginator.get_page(current_page)
    return page


def query_get_clients_list():
    # sql_query = 'select pbn_owner as item, count(pbn_owner) as count from clients_pbn_sites_and_articles_new group by pbn_owner order by count desc'
    sql_query = 'select client_name as item from clients order by client_name'
    return execute_select_query(sql_query)


def query_get_money_sites_list(clients=None):
    sql_query = 'SELECT DISTINCT acceptor_domain  as item FROM urls_check_new'
    where_clause, where_params = generate_where_clause(clients)
    if where_clause is not None:
        sql_query += ' where ' + where_clause
    return execute_select_query(sql_query, where_params)


def query_get_deadline_data(clients=None, money_sites=None):
    sql_query = 'SELECT MAX(deadline) as deadline, DATEDIFF(MAX(deadline), CURRENT_DATE) as diff FROM plan_fact'
    where_clause, where_params = generate_where_clause(clients, money_sites)
    if where_clause is not None:
        sql_query += ' where ' + where_clause
    return execute_select_query(sql_query, where_params)

# Новых PBN-доменов
def query_get_new_domains(clients=None, date_start=None, date_end=None):
    sql_query = 'select count(distinct id_site) as new_domains from clients_pbn_sites_and_articles_new '

    where_clause, where_params = generate_where_clause(clients=clients, date_create_start=date_start, date_create_end=date_end)
    if where_clause is not None:
        sql_query += ' where ' + where_clause

    # print(sql_query, where_params)

    return execute_select_query(sql_query, where_params, True)


def query_get_new_publications(clients=None, date_start=None, date_end=None):
    sql_query = 'select count( distinct article_url) as count from clients_pbn_sites_and_articles_new'
    where_clause, where_params = generate_where_clause(clients, date_create_start=date_start, date_create_end=date_end)
    if where_clause is not None:
        sql_query += ' where ' + where_clause

    # print(sql_query, where_params)

    return execute_select_query(sql_query, where_params, True)


def query_get_new_pbn_domains(clients=None, money_sites=None):
    sql_query = 'SELECT MAX(`site_url`) max_site_url,  SUM(pbn_sites) as sum_pbn_sites, round(MAX(site_url)/SUM(pbn_sites)*100, 1) as progress_bar FROM `plan_fact`'
    where_clause, where_params = generate_where_clause(clients, None, money_sites)
    if where_clause is not None:
        sql_query += ' where ' + where_clause
    # print(sql_query, where_params)
    return execute_select_query(sql_query, where_params, True)


def query_get_links_to_money_sites(clients=None, money_sites=None):
    sql_query = 'SELECT SUM(links_fact) as summ_url_to_acceptor, SUM(links) as summ_links , floor(SUM(links_fact)/SUM(links)*100) as progress FROM plan_fact'
    where_clause, where_params = generate_where_clause(clients, None, money_sites)
    if where_clause is not None:
        sql_query += ' where ' + where_clause
    # print(sql_query,where_params)
    return execute_select_query(sql_query, where_params, True)


def query_get_chart_data(clients=None, money_sites=None):
    sql_query = 'SELECT pbn_owner, date(site_create) as x, count(DISTINCT site_url) as y  FROM clients_pbn_sites_and_articles_new :where GROUP BY pbn_owner, date(site_create);'
    where_clause, where_params = generate_where_clause(clients, money_sites)
    if where_clause is not None:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')
    # print(sql_query,where_params)
    return execute_select_query(sql_query, where_params)


def query_get_pbn_domains(clients=None, money_sites=None, current_page=1, items_per_page=20):
    sql_query = 'SELECT pbn_owner, site_url, site_create, COUNT(site_url) as count_article, MAX(date_create) as last_update, DATEDIFF(CURRENT_DATE,MAX(date_create)) as date_diff ' \
                'FROM clients_pbn_sites_and_articles_new ' \
                ':where ' \
                'GROUP by pbn_owner, site_url, site_create'
    where_clause, where_params = generate_where_clause(clients)
    if where_clause is not None:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')

    # print(sql_query, where_params)
    # print(current_page, items_per_page)

    return get_paginator(sql_query, where_params, current_page, items_per_page)


def query_links_to_money_sites(clients=None, money_sites=None, current_page=1, items_per_page=20):
    sql_query = 'SELECT url_from_donor, anchor_value, url_to_acceptor FROM urls_check_new'
    where_clause, where_params = generate_where_clause(clients=clients, acceptor_domains=money_sites)
    if where_clause is not None:
        sql_query += ' where ' + where_clause
    return get_paginator(sql_query, where_params, current_page, items_per_page)


def query_anchor_links(clients=None, money_sites=None, query_type=1, current_page=1, items_per_page=20000):

    if query_type == 1:
        sql_query = 'SELECT anchor_value, COUNT(url_from_donor) as count_url_from_donor FROM urls_check_new :where GROUP by anchor_value'
    else:
        sql_query = 'SELECT anchor_value, acceptor_domain, COUNT(url_from_donor) as count_url_from_donor FROM urls_check_new :where GROUP by anchor_value,acceptor_domain'

    where_clause, where_params = generate_where_clause(clients=clients, acceptor_domains=money_sites)

    if where_clause is not None:
        # sql_query = sql_query.replace(':where', ' where ' + where_clause + ' and date_check = CURRENT_DATE')
        sql_query = sql_query.replace(':where', ' where ' + where_clause + ' and date_check = (select max(`date_check`) from `urls_check_new`)')
    else:
        # sql_query = sql_query.replace(':where', 'date_check = CURRENT_DATE')
        sql_query = sql_query.replace(':where', ' where date_check = (select max(`date_check`) from `urls_check_new`)')

    # print(sql_query)

    return get_paginator(sql_query, where_params, current_page, items_per_page)


def generate_where_clause(clients=None, money_sites=None, acceptor_domains=None, date_start=None, date_end=None, date_create_start=None, date_create_end=None):
    where_params = []
    where_clause = []

    # print(date_start, date_end)

    if clients is not None and len(clients) > 0:
        clients_array = clients.split(',')
        clients_placeholder = ','.join(['%s'] * len(clients_array))
        where_clause.append("pbn_owner IN (" + clients_placeholder + ')')
        where_params += clients_array

    if money_sites:
        money_sites_array = money_sites.split(',')
        clients_placeholder = ','.join(['%s'] * len(money_sites_array))
        where_clause.append("site_url IN (" + clients_placeholder + ')')
        where_params += money_sites_array

    if acceptor_domains:
        acceptor_domains_array = acceptor_domains.split(',')
        clients_placeholder = ','.join(['%s'] * len(acceptor_domains_array))
        where_clause.append("acceptor_domain IN (" + clients_placeholder + ')')
        where_params += acceptor_domains_array

    if date_start:
        where_params.append(date_start)
        where_clause.append("check_date >= %s")

    if date_end:
        where_params.append(date_end)
        where_clause.append("check_date <= %s")

    if date_create_start:
        where_params.append(date_create_start)
        where_clause.append("date_create >= %s")

    if date_create_end:
        where_params.append(date_create_end)
        where_clause.append("date_create <= %s")

    if len(where_clause) > 0:
        where_clause = ' AND '.join(where_clause)
    else:
        where_clause = None

    return where_clause, where_params


def query_summary():
    sql_query = 'SELECT ' \
        'pp.client, ' \
        'cp2.site_url, ' \
        'pp.money_site, ' \
        'cp.site_url_money, ' \
        'pp.pbn_sites, ' \
        '(IFNULL(sum(pp.pbn_sites) - ifnull(SUM(cp.site_url_money), SUM(site_url)), SUM(pp.pbn_sites))) AS rest_domains, ' \
        'uc.links_fact, ' \
        'pp.links, ' \
        '(IFNULL(sum(links) - sum(links_fact), SUM(links))) AS rest_links, ' \
        'DATEDIFF(deadline, CURRENT_DATE) ' \
        'FROM ' \
            'pbn_plans pp ' \
                'LEFT JOIN ' \
                    '( ' \
                        'SELECT pbn_owner, COUNT(DISTINCT site_url) AS site_url_money ' \
                        'FROM clients_pbn_sites_and_articles_new ' \
                        'GROUP BY pbn_owner ' \
                    ') cp ON pp.money_site = cp.pbn_owner ' \
                'LEFT JOIN ' \
                    '( ' \
                        'SELECT COUNT(url_to_acceptor) as links_fact, pbn_owner, acceptor_domain ' \
                        'FROM urls_check_new WHERE date_check = (select max(`date_check`) from `urls_check_new`) ' \
                        'GROUP BY pbn_owner, acceptor_domain ' \
                    ') uc ON cp.pbn_owner = uc.pbn_owner AND uc.acceptor_domain = pp.money_site ' \
                'LEFT JOIN ' \
                    '( ' \
                        'SELECT pbn_owner, COUNT(DISTINCT site_url) AS site_url ' \
                        'FROM clients_pbn_sites_and_articles_new ' \
                        'GROUP BY pbn_owner ' \
                    ') cp2 ON pp.client =cp2.pbn_owner ' \
        'GROUP BY pp.client, pp.money_site'

    data = execute_select_query(sql_query)

    prev = ''

    i = 0;

    while i < len(data):
        print(data[i])
        print(data[i]['client'])
        if prev == data[i]['client']:
            data[i]['client'] = ''

        prev = data[i]['client']
        i += 1

    return data
