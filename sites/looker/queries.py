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


def clients_pbn_sites_and_articles_new(client_id=None, current_page=1, items_per_page=20):
    sql_query = "SELECT ps.id as id_site, ps.site_url, ps.date_create as site_create, ps.id_server, s.server_name, c.id as id_client, c.client_name as pbn_owner, tbl.id_pbn_site, tbl.date_create, tbl.date_modified, tbl.article_url, tbl.article_name, lad.domain_name as acceptor_domain FROM pbn_sites ps LEFT JOIN servers s ON ps.id_server = s.id LEFT JOIN clients c ON c.id = s.client_id LEFT JOIN(SELECT pa.id_pbn_site, pa.date_create, pa.date_modified, pa.article_name, CONCAT('https://', pa.article_url, '/') as article_url FROM pbn_articles pa) tbl ON tbl.id_pbn_site = ps.id LEFT JOIN links_all_urls lau ON tbl.article_url = lau.url LEFT JOIN (SELECT * FROM links_check_donor_acceptor lcda WHERE date_check = CURRENT_DATE()) lcda2 ON lau.id = lcda2.id_url_from_donor LEFT JOIN links_all_urls lau2 ON lcda2.id_url_to_acceptor = lau2.id LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id"
    if (client_id != None ):
        sql_query += ' c.id =' + int(client_id)
        return get_paginator(sql_query, None, current_page, items_per_page)


def urls_check_new(client_id=None, current_page=1, items_per_page=20):
    sql_query = 'SELECT lcda.id_url_from_donor, lau.url AS url_from_donor, lad.domain_name AS donor_domain, lau.date_add AS donor_date_add, lcda.id_url_to_acceptor, lau2.url AS url_to_acceptor, lad2.domain_name AS acceptor_domain, cn.client_name AS client_name, c2.client_name AS pbn_owner, s.client_id, lau2.date_add AS acceptor_date_add, laa.anchor_value, laa.date_add AS anchor_date_add, lcda.date_check FROM links_check_donor_acceptor lcda LEFT JOIN links_all_urls lau ON lcda.id_url_from_donor = lau.id LEFT JOIN links_all_urls lau2 ON lcda.id_url_to_acceptor = lau2.id LEFT JOIN links_all_anchors laa ON lcda.id_anchor = laa.id LEFT JOIN links_all_domains lad ON lau.id_domain = lad.id LEFT JOIN links_all_domains lad2 ON lau2.id_domain = lad2.id LEFT JOIN relation_pbn_sites_links_all_domains rpslad ON lad.id = rpslad.id_links_all_domains LEFT JOIN pbn_sites ps ON rpslad.id_pbn_sites = ps.id LEFT JOIN servers s ON ps.id_server = s.id LEFT JOIN clients c2 ON s.client_id = c2.id LEFT JOIN( SELECT id, client_name, SUBSTRING_INDEX(client_name, ' / ', 1) AS client_domain, date_add FROM clients c UNION SELECT id, client_name, SUBSTRING_INDEX(client_name, ' / ', -1) AS client_domain, date_add FROM clients c) cn ON lad2.domain_name = cn.client_domain WHERE c2.id = c1.id';
    if (client_id != None):
        sql_query += ' and c2.id=' + int(client_id)
    return get_paginator(sql_query, None, current_page, items_per_page)
