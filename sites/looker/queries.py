from django.core.paginator import Paginator
from django.db import connections, connection
from django.db.models import Q

from .settings import DB


def execute_select_query(query, params=None, fetch_single=False):
    with connections[DB].cursor() as cursor:
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
    with connections[DB].cursor() as cursor:
        cursor.execute(query, params)
        affected_rows = cursor.rowcount
    return affected_rows


def get_query_result(query, params=None):
    with connections[DB].cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
    return results


def get_paginator(sql_query, params, current_page=1, items_per_page=20):
    results = get_query_result(sql_query, params)
    paginator = Paginator(results, items_per_page)
    page = paginator.get_page(current_page)
    return page


def generate_where_clause(client_id=None, money_sites=None, date_start=None, date_end=None):
    where_params = []
    where_clause = []

    if client_id is not None:
        where_params.append(client_id)
        where_clause.append("client_id = %s")

    if money_sites:
        where_params.append(money_sites)
        where_clause.append(f"acceptor_domain IN (%s)")

    if date_start:
        where_params.append(date_start)
        where_clause.append("check_date >= %s")

    if date_end:
        where_params.append(date_end)
        where_clause.append("check_date <= %s")

    where_clause = ' AND '.join(where_clause)
    return where_clause, where_params


# for filters
def get_client_list():
    sql_query = 'SELECT pbn_owner as id, pbn_owner as name FROM clients_pbn_sites_and_articles_new GROUP BY pbn_owner'
    return execute_select_query(sql_query, None)


def get_money_sites_lists(client_id=None):
    params = None
    sql_query = 'SELECT acceptor_domain_id as id, acceptor_domain as name FROM urls_check_new :where GROUP BY acceptor_domain_id'
    where_clause, where_params = generate_where_clause(client_id=client_id)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')

    return execute_select_query(sql_query, where_params)


# chart
def get_chart_data(client_id=None, money_sites_id=None):
    sql_query = "SELECT pbn_owner AS label, DATE(site_create) AS x, COUNT(site_url) AS y FROM clients_pbn_sites_and_articles_new :where GROUP BY label, DATE(site_create)  order by  DATE(site_create) asc"
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites_id)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', ' ')

    return execute_select_query(sql_query, where_params)


# Сводка

def get_count_new_domains(client_id=None, money_sites=None, date_start=None, date_end=None):
    sql_query = 'SELECT DISTINCT COUNT(id_site) as count FROM clients_pbn_sites_and_articles_new :where'
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites,
                                                       date_start=date_start, date_end=date_end)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')
    return execute_select_query(query=sql_query, params=where_params, fetch_single=True)


def get_count_publications(client_id=None, money_sites=None):
    sql_query = 'SELECT COUNT(distinct id_article) as count FROM clients_pbn_sites_and_articles_new :where'
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')
    return execute_select_query(query=sql_query, params=where_params, fetch_single=True)


def get_count_new_publications(client_id=None, money_sites=None, date_start=None, date_end=None):
    sql_query = 'SELECT COUNT(distinct id_article) as count FROM clients_pbn_sites_and_articles_new :where'
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites,
                                                       date_start=date_start, date_end=date_end)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', ' ')

    return execute_select_query(query=sql_query, params=where_params, fetch_single=True)


# PBN-доменов - MAX(site_url), целевое значение SUM(pbn_sites) из plan_fact,
# прогресс бар показывает MAX(site_url)/SUM(pbn_sites)*100
# Фильтруется по клиенту и money-site
# Не фильтруется по дате
def get_count_pbn_domains(client_id=None, money_sites=None):
    sql_query = 'SELECT DISTINCT COUNT(article_url) as count FROM clients_pbn_sites_and_articles_new :where'
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites)
    if where_clause:
        sql_query = sql_query.replace(':where', ' where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')
    return execute_select_query(query=sql_query, params=where_params, fetch_single=True)


# TABLE
def get_domain_pbn_and_publications(client_id=None, money_sites=None, start_date=None, date_end=None, current_page=1,
                                    items_per_page=10):
    sql_query = "SELECT pbn_owner, site_url, date(site_create) as site_create, COUNT(id_article) as count_article_url, MAX(date(date_create)) as date_created, DATEDIFF( CURRENT_DATE(), MAX(date_create)) as date_diff FROM clients_pbn_sites_and_articles_new :where GROUP BY pbn_owner, site_url, date(site_create)"
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites,
                                                       date_start=start_date, date_end=date_end)
    if where_clause:
        sql_query = sql_query.replace(':where', 'where ' + where_clause)
    else:
        sql_query = sql_query.replace(':where', '')

    return get_paginator(sql_query, where_params, current_page=current_page, items_per_page=items_per_page)


def get_links_to_money_sites(client_id=None, money_sites=None, current_page=1,
                             items_per_page=10):
    sql_query = "SELECT distinct url_from_donor, anchor_value, url_to_acceptor FROM urls_check_new where date_check=CURRENT_DATE() :and"
    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites)
    if where_clause:
        sql_query = sql_query.replace(':and', ' and '+where_clause)
    else:
        sql_query = sql_query.replace(':and', '')
    return get_paginator(sql_query, where_params, current_page=current_page, items_per_page=items_per_page)


def get_anchor_lists(client_id=None, money_sites=None, current_page=1,
                     items_per_page=10, stage=0):
    if stage == 0:
        sql_query = "SELECT anchor_value, COUNT(url_from_donor) as count FROM urls_check_new where date_check=CURRENT_DATE() :and group by anchor_value"
    else:
        sql_query = "SELECT anchor_value, acceptor_domain, COUNT(url_from_donor) as count FROM urls_check_new where date_check=CURRENT_DATE() :and  group by anchor_value, acceptor_domain"

    where_clause, where_params = generate_where_clause(client_id=client_id, money_sites=money_sites)
    if where_clause:
        sql_query = sql_query.replace(':and', ' and '+where_clause)
    else:
        sql_query = sql_query.replace(':and', '')
    print(sql_query)
    print(where_params)
    return get_paginator(sql_query, where_params, current_page=current_page, items_per_page=items_per_page)
