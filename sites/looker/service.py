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


def get_domain_and_pbn_publications(page_number, items_per_page=10):
    sql_query = "SELECT c.client_name AS client_name, d.domain_name AS pbn_domain, date(s.date_create) as date_create, COUNT(a.id_row) AS total_publications, MAX(date(a.date_modified)) AS last_post, DATEDIFF(CURDATE(), MAX(a.date_modified)) AS day_since_last_publication FROM links_all_domains d INNER JOIN relation_pbn_sites_links_all_domains r ON d.id = r.id_links_all_domains INNER JOIN pbn_sites s ON r.id_pbn_sites = s.id INNER JOIN pbn_articles a ON s.id = a.id_pbn_site INNER JOIN money_sites m ON s.id = m.id_row INNER JOIN clients c ON m.client_id = c.id GROUP BY c.client_name, d.domain_name, s.date_create ORDER BY c.client_name, d.domain_name;"
    results = get_query_result(sql_query)
    paginator = Paginator(results, items_per_page)
    page = paginator.get_page(page_number)
    return page


def get_publications_by_client(client_id=None):
    sql_query = "SELECT c.id as client_id, c.client_name, DATE(a.date_modified) AS publication_date, COUNT(a.id_row) AS publication_count FROM pbn_articles a INNER JOIN pbn_sites s ON a.id_pbn_site = s.id INNER JOIN servers srv ON srv.id = s.id_server INNER JOIN clients c ON c.id = srv.client_id"
    params = None
    if client_id != None:
        sql_query += " where c.client_id= %d"
        params = [client_id]
    sql_query += ' GROUP BY c.id, publication_date ORDER BY  c.id, publication_date ASC'
    return execute_select_query(sql_query, params)


def get_links_to_money_sites(page_number, items_per_page=10):
    sql_query = "SELECT lca.id AS link_id, lau_don.url AS donor_url, lau_acc.url AS acceptor_url, laa.anchor_value AS anchor FROM links_check_donor_acceptor lca INNER JOIN links_all_urls lau_don ON lca.id_url_from_donor = lau_don.id INNER JOIN links_all_urls lau_acc ON lca.id_url_to_acceptor = lau_acc.id LEFT JOIN links_all_anchors laa ON lca.id_anchor = laa.id INNER JOIN links_all_domains lad_don ON lau_don.id_domain = lad_don.id INNER JOIN links_all_domains lad_acc ON lau_acc.id_domain = lad_acc.id INNER JOIN money_sites ms ON lad_don.id = ms.id_domain OR lad_acc.id = ms.id_domain;";
    results = get_query_result(sql_query)
    paginator = Paginator(results, items_per_page)
    page = paginator.get_page(page_number)
    return page


def get_count_anchor_by_url(page_number, items_per_page=10):
    sql_query = "SELECT la.anchor_value, laa.domain_name AS accepted_domain, COUNT(la.id) AS url_count FROM links_all_anchors la JOIN links_check_donor_acceptor lcda ON la.id = lcda.id_anchor JOIN links_all_urls lau ON lcda.id_url_to_acceptor = lau.id JOIN links_all_domains laa ON lau.id_domain = laa.id GROUP BY la.anchor_value, laa.domain_name ORDER BY `url_count` DESC"
    results = get_query_result(sql_query)
    paginator = Paginator(results, items_per_page)
    page = paginator.get_page(page_number)
    return page


def filter_objects(model, filters):
    query = Q()
    for field, value in filters.items():
        query &= Q(**{field: value})
    filtered_objects = model.objects.filter(query)
    data = [obj.to_json() for obj in filtered_objects]
    return data
