from django.db import models
from django.conf import settings

class LookerBaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if 'looker_db' in settings.DATABASES:
            self._state.db = 'looker_db'
        super().save(*args, **kwargs)


class Clients(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    client_name = models.CharField(max_length=128, null=True, default=None)
    date_add = models.DateField(null=True, default=None)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.client_name,
            'date_add': str(self.date_add) if self.date_add else None,
        }

    class Meta:
        db_table = 'clients'


class Servers(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    server_name = models.CharField(max_length=64, null=True, default=None)
    ip_server = models.CharField(max_length=15, null=True, default=None)
    date_add = models.DateField(null=True, default=None)
    client = models.ForeignKey(Clients, null=True, default=None, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.server_name,
            'ip': self.ip_server,
            'date_add': str(self.date_add) if self.date_add else None,
            'client': self.client.to_json() if self.client else None,
        }

    class Meta:
        db_table = 'servers'


class LinksAllAnchors(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    anchor_value = models.TextField()
    date_add = models.DateField(null=True, default=None)

    def to_json(self):
        return {
            'id': self.id,
            'value': self.anchor_value,
            'date_add': str(self.date_add) if self.date_add else None,
        }

    class Meta:
        db_table = 'links_all_anchors'


class LinksAllDomains(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    domain_name = models.CharField(max_length=128, null=True, default=None)
    date_add = models.DateField(null=True, default=None)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.domain_name,
            'date_add': str(self.date_add) if self.date_add else None,
        }

    class Meta:
        db_table = 'links_all_domains'


class LinksAllUrls(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    url = models.TextField()
    date_add = models.DateField(null=True, default=None)
    domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'date_add': str(self.date_add) if self.date_add else None,
            'domain': self.domain.to_json() if self.domain else None,
        }

    class Meta:
        db_table = 'links_all_urls'


class LinksCheckDonorAcceptor(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    date_check = models.DateField(null=True, default=None)
    donor_url = models.ForeignKey(LinksAllUrls, related_name='donor_links', on_delete=models.CASCADE)
    acceptor_url = models.ForeignKey(LinksAllUrls, related_name='acceptor_links', on_delete=models.CASCADE)
    anchor = models.ForeignKey(LinksAllAnchors, null=True, default=None, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id,
            'date_check': str(self.date_check) if self.date_check else None,
            'donor': self.donor_url.to_json() if self.donor_url else None,
            'acceptor': self.acceptor_url.to_json() if self.acceptor_url else None,
            'anchor': self.anchor.to_json() if self.anchor else None,
        }

    class Meta:
        db_table = 'links_check_donor_acceptor'


class PbnSites(LookerBaseModel):
    id = models.IntegerField(primary_key=True)
    site_url = models.CharField(max_length=128, null=True, default=None)
    date_create = models.DateTimeField(null=True, default=None)
    server = models.ForeignKey(Servers, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id,
            'site_url': self.site_url,
            'date_create': str(self.date_create) if self.date_create else None,
            'server': self.server.to_json() if self.server else None,
        }

    class Meta:
        db_table = 'pbn_sites'


class RelationPbnSitesLinksAllDomains(LookerBaseModel):
    pbn_site = models.ForeignKey(PbnSites, on_delete=models.CASCADE)
    links_all_domain = models.ForeignKey(LinksAllDomains, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'pbn_site': self.pbn_site.to_json() if self.pbn_site else None,
            'links_all_domain': self.links_all_domain.to_json() if self.links_all_domain else None,
        }

    class Meta:
        db_table = 'relation_pbn_sites_links_all_domains'


class MoneySites(LookerBaseModel):
    id_row = models.IntegerField(primary_key=True)
    site_url = models.CharField(max_length=100, null=True, default=None)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    domain = models.ForeignKey(LinksAllDomains, null=True, db_column='id_domain', default=None,
                               on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id_row,
            'site_url': self.site_url,
            'client': self.client.to_json() if self.client else None,
            'domain': self.domain.to_json() if self.domain else None,
        }

    class Meta:
        db_table = 'money_sites'


class PbnArticles(LookerBaseModel):
    id_row = models.IntegerField(primary_key=True)
    id_article = models.IntegerField()
    date_create = models.DateTimeField(null=True, default=None)
    date_modified = models.DateTimeField(null=True, default=None)
    text_article = models.TextField()
    article_name = models.TextField()
    article_url = models.TextField()
    pbn_site = models.ForeignKey(PbnSites, on_delete=models.CASCADE)

    def to_json(self):
        return {
            'id': self.id_row,
            'id_article': self.id_article,
            'date_create': str(self.date_create) if self.date_create else None,
            'date_modified': str(self.date_modified) if self.date_modified else None,
            'text_article': self.text_article,
            'article_name': self.article_name,
            'article_url': self.article_url,
            'pbn_site': self.pbn_site.to_json() if self.pbn_site else None,
        }

    class Meta:
        db_table = 'pbn_articles'
