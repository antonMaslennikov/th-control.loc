SELECT
    ps.id AS id_site,
    ps.site_url,
    ps.date_create AS site_create,
    CONCAT('https://', pa.article_url, '/') AS article_url,
    pa.date_create,
    CASE WHEN c.client_name = 'old' AND lad.domain_name LIKE '%fonbet%' THEN 'fonbet.by/fonbet.kz' WHEN c.client_name = 'old' THEN lad.domain_name ELSE c.client_name
END AS pbn_owner
FROM
    pbn_sites ps
LEFT JOIN servers s ON
    ps.id_server = s.id
LEFT JOIN clients c ON
    c.id = s.client_id
LEFT JOIN(
    SELECT pa.id_pbn_site,
        pa.date_create,
        CONCAT('https://', pa.article_url, '/') AS article_url
    FROM
        pbn_articles pa
) pa
ON
    pa.id_pbn_site = ps.id
LEFT JOIN links_all_domains lad ON
    lad.id = pa.id_pbn_site
