DELIMITER //

CREATE DEFINER=`root`@`%` PROCEDURE `RECREATE_TABLE_FOR_LOOKER_STUDIO`()
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

    // -----------------------------------------------------------------------------------------------------------------

    DROP TABLE IF EXISTS clients_pbn_sites_and_articles_new;

    CREATE TABLE clients_pbn_sites_and_articles_new as
        SELECT DISTINCT pa.date_create, pa.id_article, ps.id as id_site, ps.site_url, ps.date_create AS site_create, COALESCE( CASE WHEN s.id = 4 AND lad.domain_name LIKE '%fonbet%' THEN 'fonbet.by/fonbet.kz' WHEN s.id = 4 THEN lad.domain_name ELSE c.client_name END, '' ) AS pbn_owner
        FROM pbn_articles pa
            JOIN pbn_sites ps ON pa.id_pbn_site = ps.id
            JOIN servers s ON ps.id_server = s.id
            JOIN clients c ON s.client_id = c.id
            LEFT JOIN links_all_urls lau ON ( REPLACE ( REPLACE ( CASE WHEN RIGHT(url, 1) = '/' THEN SUBSTRING(url, 1, LENGTH(url) - 1) ELSE url END, 'https://', '' ), 'http://', '' ) ) = pa.article_url
            LEFT JOIN links_check_donor_acceptor lcda ON lau.id = lcda.id_url_from_donor AND lcda.date_check = CURRENT_DATE
            LEFT JOIN links_all_urls lau2 ON lcda.id_url_to_acceptor = lau2.id
            LEFT JOIN links_all_domains lad ON lau2.id_domain = lad.id;

    CREATE INDEX idx_clients_pbn_sites_and_articles_new_pbn_owner ON clients_pbn_sites_and_articles_new (pbn_owner);

    // -----------------------------------------------------------------------------------------------------------------

    DROP TABLE IF EXISTS urls_check_new;

    CREATE TABLE urls_check_new as
        SELECT lcda.date_check, lad.domain_name AS donor_domain, lau.url AS url_from_donor, laa.anchor_value, lau2.url AS url_to_acceptor, lad2.domain_name AS acceptor_domain, COALESCE( CASE WHEN c.client_name = 'old' AND lad2.domain_name LIKE 'fonbet%' THEN 'fonbet.by/fonbet.kz' WHEN c.client_name = 'old' THEN lad2.domain_name ELSE c.client_name END, lad2.domain_name) AS pbn_owner
        FROM links_check_donor_acceptor lcda
            JOIN links_all_urls lau ON lcda.id_url_from_donor = lau.id
            JOIN links_all_urls lau2 ON lcda.id_url_to_acceptor = lau2.id
            JOIN links_all_anchors laa ON lcda.id_anchor = laa.id
            JOIN links_all_domains lad ON lau.id_domain = lad.id
            JOIN links_all_domains lad2 ON lau2.id_domain = lad2.id
            LEFT JOIN relation_pbn_sites_links_all_domains rpslad ON lad.id = rpslad.id_links_all_domains
            LEFT JOIN pbn_sites ps ON rpslad.id_pbn_sites = ps.id
            LEFT JOIN servers s ON ps.id_server = s.id
            LEFT JOIN clients c ON s.client_id = c.id;

    CREATE INDEX idx_urls_check_new_pbn_owner ON urls_check_new (pbn_owner);
    CREATE INDEX idx_urls_check_new_date_check ON urls_check_new (date_check);
    CREATE INDEX idx_urls_check_new_acceptor_domain ON urls_check_new (date_check, acceptor_domain);

    // -----------------------------------------------------------------------------------------------------------------

    DROP TABLE IF EXISTS plan_fact;

    CREATE TABLE plan_fact as
        SELECT
            cp.pbn_owner,
            cp.site_url AS count_site_url,
            uc.acceptor_domain,
            uc.count_url_to_acceptor,
            pp.pbn_sites,
            pp.links,
            pp.deadline
        FROM
            (
                SELECT pbn_owner, COUNT(DISTINCT site_url) AS site_url
                FROM clients_pbn_sites_and_articles_new
                GROUP BY pbn_owner
            ) cp
                JOIN (SELECT pbn_owner, acceptor_domain, COUNT(url_to_acceptor) AS count_url_to_acceptor FROM urls_check_new WHERE date_check = CURRENT_DATE() GROUP BY pbn_owner, acceptor_domain ) uc ON cp.pbn_owner = uc.pbn_owner
                LEFT JOIN ( SELECT pbn_sites, links, deadline, money_site FROM pbn_plans WHERE money_site IS NOT NULL ) pp ON uc.acceptor_domain = pp.money_site;

    CREATE INDEX idx_plan_fact_pbn_owner ON plan_fact (pbn_owner);
    CREATE INDEX idx_plan_fact_acceptor_domain ON plan_fact (acceptor_domain);
END//

DELIMITER ;

CREATE EVENT RECREATE_TABLE_FOR_LOOKER_STUDIO
ON SCHEDULE EVERY 6 HOUR
STARTS CURRENT_TIMESTAMP
DO call RECREATE_TABLE_FOR_LOOKER_STUDIO();

SET GLOBAL event_scheduler=ON;