DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `RECREATE_TABLE_FOR_LOOKER_STUDIO`()
	NOT DETERMINISTIC
	CONTAINS SQL
	SQL SECURITY DEFINER
BEGIN

    CREATE TABLE IF NOT EXISTS pbn_plans(
        id int PRIMARY KEY AUTO_INCREMENT ,
        client varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        money_site varchar(255) DEFAULT NULL,
        pbn_sites int DEFAULT NULL,
        links int DEFAULT NULL,
        deadline date DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




    DROP TABLE IF EXISTS clients_pbn_sites_and_articles_new;

    CREATE TABLE clients_pbn_sites_and_articles_new as
        WITH pbn_domains AS (
            SELECT
                CASE
                    WHEN pbn_owner_temp = 'old' AND acceptor_domain LIKE '%fonbet%' THEN 'fonbet.by/fonbet.kz'
                    WHEN pbn_owner_temp = 'old' AND acceptor_domain IS NOT NULL THEN acceptor_domain
                    ELSE pbn_owner_temp
                END as pbn_owner, id_site
            FROM (
                SELECT ps.id as id_site, ps.site_url, ps.date_create as site_create,
                    ps.id_server, s.server_name, c.id as id_client, c.client_name as pbn_owner_temp,
                    tbl.id_pbn_site, tbl.date_create, tbl.date_modified,
                    tbl.article_url, tbl.article_name, lad.domain_name as acceptor_domain
                FROM
                    pbn_sites ps
                        LEFT JOIN servers s ON ps.id_server = s.id
                        LEFT JOIN clients c ON c.id = s.client_id
                        LEFT JOIN (
                                SELECT pa.id_pbn_site, pa.date_create, pa.date_modified, pa.article_name, CONCAT('https://', pa.article_url, '/') as article_url
                                FROM pbn_articles pa
                            ) tbl ON tbl.id_pbn_site = ps.id
                        LEFT JOIN links_all_urls lau ON tbl.article_url = lau.url
                        LEFT JOIN (
                                SELECT *
                                FROM links_check_donor_acceptor lcda
                                WHERE date_check = (select max(`date_check`) from `links_check_donor_acceptor`)
                            ) lcda2 ON lau.id = lcda2.id_url_from_donor
                        LEFT JOIN links_all_urls lau2 ON lcda2.id_url_to_acceptor = lau2.id
                        LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id
                ) pzdc
            GROUP BY pbn_owner, id_site
        )

        SELECT articles_new.id_site, site_url, site_create, article_url, article_length, article_name, count_h1_h2, date_create, pbn_owner
        FROM
            (
                SELECT pzdc.id_site, pzdc.site_url, pzdc.site_create, pzdc.article_url, pzdc.article_length, pzdc.count_h1_h2, pzdc.article_name, pzdc.date_create
                FROM (
                    SELECT ps.id as id_site, ps.site_url, ps.date_create as site_create,
                        ps.id_server, s.server_name, c.id as id_client, c.client_name as pbn_owner_temp,
                        tbl.id_pbn_site, tbl.date_create, tbl.date_modified,
                        tbl.article_url, tbl.article_length, tbl.count_h1_h2, tbl.article_name, lad.domain_name as acceptor_domain
                    FROM pbn_sites ps
                        LEFT JOIN servers s ON ps.id_server = s.id
                        LEFT JOIN clients c ON c.id = s.client_id
                        LEFT JOIN (
                                SELECT pa.id_pbn_site, pa.date_create, pa.date_modified, pa.article_name,
                                    CONCAT('https://', pa.article_url, '/') as article_url,
                                    (CHAR_LENGTH(text_article) - CHAR_LENGTH(REGEXP_REPLACE(text_article, '</h1>|</h2>', ''))) / CHAR_LENGTH('</h1>') AS count_h1_h2,
                                    CHAR_LENGTH(REGEXP_REPLACE(text_article, '<[^>]*>| ', '')) as article_length
                                FROM pbn_articles pa
                            ) tbl ON tbl.id_pbn_site = ps.id
                        LEFT JOIN links_all_urls lau ON tbl.article_url = lau.url
                        LEFT JOIN (
                                SELECT *
                                FROM links_check_donor_acceptor lcda
                                WHERE date_check = (select max(`date_check`) from `links_check_donor_acceptor`)
                            ) lcda2 ON lau.id = lcda2.id_url_from_donor
                        LEFT JOIN links_all_urls lau2 ON lcda2.id_url_to_acceptor = lau2.id
                        LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id) pzdc
            ) articles_new
                JOIN pbn_domains ON pbn_domains.id_site = articles_new.id_site
        GROUP BY articles_new.id_site, site_url, site_create, article_url, date_create, pbn_owner;

    CREATE INDEX idx_clients_pbn_sites_and_articles_new_pbn_owner ON clients_pbn_sites_and_articles_new (pbn_owner);




    DROP TABLE IF EXISTS urls_check_new;

    CREATE TABLE urls_check_new as
        WITH pbn_domains AS (
            SELECT
                CASE
                    WHEN pbn_owner_temp = 'old' AND acceptor_domain LIKE '%fonbet%' THEN 'fonbet.by/fonbet.kz'
                    WHEN pbn_owner_temp = 'old' AND acceptor_domain IS NOT NULL THEN acceptor_domain ELSE pbn_owner_temp
                END as pbn_owner, id_site
            FROM (
                SELECT ps.id as id_site, ps.site_url, ps.date_create as site_create,
                    ps.id_server, s.server_name, c.id as id_client, c.client_name as pbn_owner_temp,
                    tbl.id_pbn_site, tbl.date_create, tbl.date_modified,
                    tbl.article_url, tbl.article_name, lad.domain_name as acceptor_domain
                FROM pbn_sites ps
                    LEFT JOIN servers s ON ps.id_server = s.id
                    LEFT JOIN clients c ON c.id = s.client_id
                    LEFT JOIN (
                            SELECT pa.id_pbn_site, pa.date_create, pa.date_modified, pa.article_name, CONCAT('https://', pa.article_url, '/') as article_url
                            FROM pbn_articles pa
                        ) tbl ON tbl.id_pbn_site = ps.id
                    LEFT JOIN links_all_urls lau ON tbl.article_url = lau.url
                    LEFT JOIN (
                            SELECT *
                            FROM links_check_donor_acceptor lcda
                            WHERE date_check = (select max(`date_check`) from `links_check_donor_acceptor`)
                        ) lcda2 ON lau.id = lcda2.id_url_from_donor
                    LEFT JOIN links_all_urls lau2 ON lcda2.id_url_to_acceptor = lau2.id
                    LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id) pzdc
                GROUP BY pbn_owner, id_site
        )

        SELECT date_check, lad.domain_name as donor_domain, lau.url as url_from_donor, laa.anchor_value,
            lau2.url as url_to_acceptor, lad2.domain_name as acceptor_domain, pbn_owner
        FROM links_check_donor_acceptor lcda
            JOIN links_all_urls lau ON lcda.id_url_from_donor = lau.id
            JOIN links_all_urls lau2 ON lcda.id_url_to_acceptor = lau2.id
            JOIN links_all_anchors laa ON lcda.id_anchor = laa.id
            JOIN links_all_domains lad ON lau.id_domain = lad.id
            JOIN links_all_domains lad2 ON lau2.id_domain = lad2.id
            JOIN relation_pbn_sites_links_all_domains rpslad ON lad.id = rpslad.id_links_all_domains
            LEFT JOIN pbn_domains pd ON pd.id_site = rpslad.id_pbn_sites
        WHERE
            date_check = (select max(`date_check`) from `links_check_donor_acceptor`);

    CREATE INDEX idx_urls_check_new_pbn_owner ON urls_check_new (pbn_owner);
    CREATE INDEX idx_urls_check_new_date_check ON urls_check_new (date_check);
    CREATE INDEX idx_urls_check_new_acceptor_domain ON urls_check_new (date_check, acceptor_domain);




    DROP TABLE IF EXISTS plan_fact;

    CREATE TABLE plan_fact as
    SELECT
        pp.client,
        cp2.site_url,
        pp.money_site,
        cp.site_url_money,
        uc.links_fact,
        pp.pbn_sites,
        pp.links,
        pp.deadline
    FROM
        pbn_plans pp
            LEFT JOIN
                (
                    SELECT pbn_owner, COUNT(DISTINCT site_url) AS site_url_money
                    FROM clients_pbn_sites_and_articles_new
                    GROUP BY pbn_owner
                ) cp ON pp.money_site = cp.pbn_owner
            LEFT JOIN
                (
                    SELECT COUNT(url_to_acceptor) as links_fact, pbn_owner, acceptor_domain
                    FROM urls_check_new WHERE date_check = (select max(`date_check`) from `urls_check_new`)
                    GROUP BY pbn_owner, acceptor_domain
                ) uc ON cp.pbn_owner = uc.pbn_owner AND uc.acceptor_domain = pp.money_site
            LEFT JOIN
                (
                    SELECT pbn_owner, COUNT(DISTINCT site_url) AS site_url
                    FROM clients_pbn_sites_and_articles_new
                    GROUP BY pbn_owner
                ) cp2 ON pp.client =cp2.pbn_owner
    GROUP BY pp.client, pp.money_site;

    CREATE INDEX idx_plan_fact_pbn_owner ON plan_fact (client);
    CREATE INDEX idx_plan_fact_acceptor_domain ON plan_fact (money_site);
END//

DELIMITER ;

CREATE EVENT RECREATE_TABLE_FOR_LOOKER_STUDIO
ON SCHEDULE EVERY 6 HOUR
STARTS CURRENT_TIMESTAMP
DO call RECREATE_TABLE_FOR_LOOKER_STUDIO();

SET GLOBAL event_scheduler=ON;