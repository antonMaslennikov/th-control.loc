from django.db import models


class Clients(models.Model):
    id = models.IntegerField(primary_key=True)
    client_name = models.CharField(max_length=128, null=True, default=None)
    date_add = models.DateField(null=True, default=None)

    class Meta:
        db_table = 'clients'


class Servers(models.Model):
    id = models.IntegerField(primary_key=True)
    server_name = models.CharField(max_length=64, null=True, default=None)
    ip_server = models.CharField(max_length=15, null=True, default=None)
    date_add = models.DateField(null=True, default=None)
    client = models.ForeignKey(Clients, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        db_table = 'servers'


class LinksAllAnchors(models.Model):
    id = models.IntegerField(primary_key=True)
    anchor_value = models.TextField()
    date_add = models.DateField(null=True, default=None)

    class Meta:
        db_table = 'links_all_anchors'


class LinksAllDomains(models.Model):
    id = models.IntegerField(primary_key=True)
    domain_name = models.CharField(max_length=128, null=True, default=None)
    date_add = models.DateField(null=True, default=None)

    class Meta:
        db_table = 'links_all_domains'


class LinksAllUrls(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField()
    date_add = models.DateField(null=True, default=None)
    domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE)

    class Meta:
        db_table = 'links_all_urls'


class LinksCheckDonorAcceptor(models.Model):
    id = models.IntegerField(primary_key=True)
    id_url_from_donor = models.IntegerField()
    id_url_to_acceptor = models.IntegerField()
    date_check = models.DateField(null=True, default=None)
    donor_url = models.ForeignKey(LinksAllUrls, related_name='donor_links', on_delete=models.CASCADE)
    acceptor_url = models.ForeignKey(LinksAllUrls, related_name='acceptor_links', on_delete=models.CASCADE)
    anchor = models.ForeignKey(LinksAllAnchors, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        db_table = 'links_check_donor_acceptor'


class MoneySites(models.Model):
    id_row = models.IntegerField(primary_key=True)
    site_url = models.CharField(max_length=100, null=True, default=None)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    domain = models.ForeignKey(LinksAllDomains, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        db_table = 'money_sites'


class PbnSites(models.Model):
    id = models.IntegerField(primary_key=True)
    site_url = models.CharField(max_length=128, null=True, default=None)
    date_create = models.DateTimeField(null=True, default=None)
    server = models.ForeignKey(Servers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pbn_sites'


class RelationPbnSitesLinksAllDomains(models.Model):
    id_pbn_sites = models.IntegerField()
    id_links_all_domains = models.IntegerField()
    pbn_site = models.ForeignKey(PbnSites, on_delete=models.CASCADE)
    links_all_domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE)

    class Meta:
        db_table = 'relation_pbn_sites_links_all_domains'


class PbnArticles(models.Model):
    id_row = models.IntegerField(primary_key=True)
    id_article = models.IntegerField()
    date_create = models.DateTimeField(null=True, default=None)
    date_modified = models.DateTimeField(null=True, default=None)
    text_article = models.TextField()
    article_name = models.TextField()
    article_url = models.TextField()
    pbn_site = models.ForeignKey(PbnSites, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pbn_articles'
