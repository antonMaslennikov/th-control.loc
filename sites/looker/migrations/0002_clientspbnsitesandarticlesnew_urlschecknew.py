from django.db import migrations


class Migration(migrations.Migration):
    operations = [
        migrations.RunSQL(
            """
            CREATE or replace  VIEW clients_pbn_sites_and_articles_new AS
            SELECT ps.id as id_site, ps.site_url, ps.date_create as site_create, 
            ps.id_server, s.server_name, c.id as id_client, c.client_name as pbn_owner,
            tbl.id_pbn_site, tbl.date_create, tbl.date_modified,
            tbl.article_url, tbl.article_name, lad.domain_name as acceptor_domain, lad.id as acceptor_domain_id
            FROM pbn_sites ps 
            LEFT JOIN servers s ON ps.id_server = s.id 
            LEFT JOIN clients c ON c.id = s.client_id 
            LEFT JOIN (SELECT id_pbn_site, date_create, date_modified, article_name, 
                CONCAT("https://", article_url, "/") as article_url
                FROM pbn_articles pa) tbl ON tbl.id_pbn_site = ps.id
            LEFT JOIN links_all_urls lau ON tbl.article_url = lau.url 
            LEFT JOIN (SELECT * 
                FROM links_check_donor_acceptor lcda 
                WHERE date_check = CURRENT_DATE()) lcda2 ON lau.id = lcda2.id_url_from_donor 
            LEFT JOIN links_all_urls lau2 ON lcda2.id_url_to_acceptor = lau2.id
            LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
        migrations.RunSQL(
            """
            CREATE or replace  VIEW urls_check_new AS
            SELECT lcda.id_url_from_donor, lau.url as url_from_donor, lad.domain_name as donor_domain, 
		lau.date_add as donor_date_add, 
		lcda.id_url_to_acceptor, lau2.url as url_to_acceptor, lad2.domain_name as acceptor_domain, lad2.id as acceptor_domain_id,
		cn.client_name as client_name, c2.client_name as pbn_owner, s.client_id,
		lau2.date_add as acceptor_date_add,
		laa.anchor_value, laa.date_add as anchor_date_add, 
		lcda.date_check	
        FROM links_check_donor_acceptor lcda  
        LEFT JOIN links_all_urls lau ON lcda.id_url_from_donor = lau.id
        LEFT JOIN links_all_urls lau2 ON lcda.id_url_to_acceptor = lau2.id 
        LEFT JOIN links_all_anchors laa ON lcda.id_anchor = laa.id
        LEFT JOIN links_all_domains lad ON lau.id_domain = lad.id 
        LEFT JOIN links_all_domains lad2 ON lau2.id_domain = lad2.id 
        LEFT JOIN relation_pbn_sites_links_all_domains rpslad ON lad.id = rpslad.id_links_all_domains
        LEFT JOIN pbn_sites ps ON rpslad.id_pbn_sites = ps.id
        LEFT JOIN servers s ON ps.id_server = s.id 
        LEFT JOIN clients c2 ON s.client_id = c2.id
        LEFT JOIN (SELECT id, client_name, SUBSTRING_INDEX(client_name, "/", 1) as client_domain, date_add 
                    FROM clients c 
                    UNION
                    SELECT id, client_name, SUBSTRING_INDEX(client_name, "/", -1) as client_domain, date_add 
                    FROM clients c) cn ON lad2.domain_name = cn.client_domain
            """,
            reverse_sql=migrations.RunSQL.noop
        )
    ]
