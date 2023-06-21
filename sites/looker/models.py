from django.db import models


class Clients(models.Model):
    client_name = models.CharField(max_length=128, blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.client_name

    class Meta:
        db_table = 'clients'


class LinksAllAnchors(models.Model):
    anchor_value = models.TextField(blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.anchor_value

    class Meta:
        db_table = 'links_all_anchors'


class LinksAllDomains(models.Model):
    domain_name = models.CharField(max_length=128, blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.domain_name

    class Meta:
        db_table = 'links_all_domains'


class LinksAllUrls(models.Model):
    url = models.TextField(blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)
    domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE, db_column='id_domain', blank=True, null=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'links_all_urls'


class LinksCheckDonorAcceptor(models.Model):
    url_from_donor = models.ForeignKey(LinksAllUrls, on_delete=models.CASCADE, db_column='id_url_from_donor')
    url_to_acceptor = models.ForeignKey(
        LinksAllUrls,
        on_delete=models.CASCADE,
        db_column='id_url_to_acceptor',
        related_name='linkscheckdonoracceptor_id_url_to_acceptor_set'
    )
    anchor = models.ForeignKey(LinksAllAnchors, on_delete=models.CASCADE, db_column='id_anchor', blank=True, null=True)
    date_check = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'links_check_donor_acceptor'
        unique_together = (('url_from_donor', 'url_to_acceptor'),)


class MoneySites(models.Model):
    site_url = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE, db_column='id_domain', blank=True, null=True)

    def __str__(self):
        return self.site_url

    class Meta:
        db_table = 'money_sites'


class PbnArticles(models.Model):
    id_article = models.IntegerField(primary_key=True)
    pbn_site = models.ForeignKey('PbnSites', on_delete=models.CASCADE, db_column='id_pbn_site')
    date_create = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    text_article = models.TextField(blank=True, null=True)
    article_name = models.TextField(blank=True, null=True)
    article_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'pbn_articles'


class PbnSites(models.Model):
    site_url = models.CharField(max_length=128, blank=True, null=True)
    date_create = models.DateTimeField(blank=True, null=True)
    server = models.ForeignKey('Servers', on_delete=models.CASCADE, db_column='id_server', blank=True, null=True)

    def __str__(self):
        return self.site_url

    class Meta:
        db_table = 'pbn_sites'


class RelationPbnSitesLinksAllDomains(models.Model):
    id_pbn_sites = models.IntegerField(primary_key=True)
    id_links_all_domains = models.IntegerField

    class Meta:
        db_table = 'relation_pbn_sites_links_all_domains'


class Servers(models.Model):
    server_name = models.CharField(max_length=64, blank=True, null=True)
    ip_server = models.CharField(max_length=15, blank=True, null=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    date_add = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.server_name

    class Meta:
        db_table = 'servers'
