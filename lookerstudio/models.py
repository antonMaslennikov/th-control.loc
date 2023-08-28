# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    client_name = models.CharField(max_length=128, blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class LinksAllAnchors(models.Model):
    anchor_value = models.TextField(blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links_all_anchors'


class LinksAllDomains(models.Model):
    domain_name = models.CharField(max_length=128, blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links_all_domains'


class LinksAllUrls(models.Model):
    url = models.TextField(blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)
    id_domain = models.ForeignKey(LinksAllDomains, models.DO_NOTHING, db_column='id_domain', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links_all_urls'


class LinksCheckDonorAcceptor(models.Model):
    id_url_from_donor = models.ForeignKey(LinksAllUrls, models.DO_NOTHING, db_column='id_url_from_donor')
    id_url_to_acceptor = models.ForeignKey(LinksAllUrls, models.DO_NOTHING, db_column='id_url_to_acceptor', related_name='linkscheckdonoracceptor_id_url_to_acceptor_set')
    id_anchor = models.ForeignKey(LinksAllAnchors, models.DO_NOTHING, db_column='id_anchor', blank=True, null=True)
    date_check = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links_check_donor_acceptor'
        unique_together = (('id', 'id_url_from_donor', 'id_url_to_acceptor'),)


class MoneySites(models.Model):
    id_row = models.AutoField(primary_key=True)
    site_url = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    id_domain = models.ForeignKey(LinksAllDomains, models.DO_NOTHING, db_column='id_domain', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'money_sites'


class PbnArticles(models.Model):
    id_row = models.AutoField(primary_key=True)  # The composite primary key (id_row, id_article, id_pbn_site) found, that is not supported. The first column is selected.
    id_article = models.IntegerField()
    id_pbn_site = models.ForeignKey('PbnSites', models.DO_NOTHING, db_column='id_pbn_site')
    date_create = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    text_article = models.TextField(blank=True, null=True)
    article_name = models.TextField(blank=True, null=True)
    article_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pbn_articles'
        unique_together = (('id_row', 'id_article', 'id_pbn_site'),)


class PbnPlans(models.Model):
    client = models.CharField(max_length=255, blank=True, null=True)
    money_site = models.CharField(max_length=255, blank=True, null=True)
    pbn_sites = models.IntegerField(blank=True, null=True)
    links = models.IntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pbn_plans'


class PbnSites(models.Model):
    site_url = models.CharField(max_length=128, blank=True, null=True)
    date_create = models.DateTimeField(blank=True, null=True)
    id_server = models.ForeignKey('Servers', models.DO_NOTHING, db_column='id_server', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pbn_sites'


class RelationPbnSitesLinksAllDomains(models.Model):
    id_pbn_sites = models.IntegerField(primary_key=True)  # The composite primary key (id_pbn_sites, id_links_all_domains) found, that is not supported. The first column is selected.
    id_links_all_domains = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'relation_pbn_sites_links_all_domains'
        unique_together = (('id_pbn_sites', 'id_links_all_domains'),)


class Servers(models.Model):
    server_name = models.CharField(max_length=64, blank=True, null=True)
    ip_server = models.CharField(max_length=15, blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servers'
