from django.db import connections
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


def get_domain_and_pbn_publications():
    sql_query = "SELECT c.client_name AS client_name, d.domain_name AS pbn_domain, s.date_create, COUNT(a.id_row) AS total_publications, MAX(a.date_modified) AS last_post, DATEDIFF(CURDATE(), MAX(a.date_modified)) AS day_since_last_publication FROM links_all_domains d INNER JOIN relation_pbn_sites_links_all_domains r ON d.id = r.id_links_all_domains INNER JOIN pbn_sites s ON r.id_pbn_sites = s.id INNER JOIN pbn_articles a ON s.id = a.id_pbn_site INNER JOIN money_sites m ON s.id = m.id_row INNER JOIN clients c ON m.client_id = c.id GROUP BY c.client_name, d.domain_name, s.date_create ORDER BY c.client_name, d.domain_name;"
    return execute_select_query(sql_query)


def get_publications_by_client(client_id=None):
    sql_query = "SELECT c.id as client_id, c.client_name, DATE(a.date_modified) AS publication_date, COUNT(a.id_row) AS publication_count FROM pbn_articles a INNER JOIN pbn_sites s ON a.id_pbn_site = s.id INNER JOIN servers srv ON srv.id = s.id_server INNER JOIN clients c ON c.id = srv.client_id"
    params = None
    if client_id != None:
        sql_query += " where c.client_id= %d"
        params = [client_id]
    sql_query += ' GROUP BY c.id, publication_date ORDER BY c.id, publication_date DESC'
    return execute_select_query(sql_query, params)


