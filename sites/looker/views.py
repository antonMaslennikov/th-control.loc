from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .service import get_domain_and_pbn_publications, get_publications_by_client

from django.http import JsonResponse
from django.views import View
from .models import (
    LinksAllDomains, LinksAllUrls, LinksCheckDonorAcceptor, PbnSites,
    RelationPbnSitesLinksAllDomains, MoneySites, PbnArticles, Servers, Clients,
)
from .settings import DB


class LinksAllDomainsAPIView(View):
    def get(self, request, domain_id=None):
        if domain_id:
            domain = LinksAllDomains.objects.using(DB).filter(id=domain_id).first()
            if domain:
                data = domain.to_json()
            else:
                data = {}
        else:
            domains = LinksAllDomains.objects.using(DB).all()
            data = [domain.to_json() for domain in domains]

        return JsonResponse(data, safe=False)


class LinksAllUrlsAPIView(View):
    def get(self, request, url_id=None):
        if url_id:
            url = LinksAllUrls.objects.using(DB).filter(id=url_id).first()
            if url:
                data = url.to_json()
            else:
                data = {}
        else:
            urls = LinksAllUrls.objects.using(DB).all()
            data = [url.to_json() for url in urls]

        return JsonResponse(data, safe=False)


class LinksCheckDonorAcceptorAPIView(View):
    def get(self, request, donor_acceptor_id=None):
        if donor_acceptor_id:
            donor_acceptor = LinksCheckDonorAcceptor.objects.using(DB).filter(id=donor_acceptor_id).first()
            if donor_acceptor:
                data = donor_acceptor.to_json()
            else:
                data = {}
        else:
            donor_acceptors = LinksCheckDonorAcceptor.objects.using(DB).all()
            data = [da.to_json() for da in donor_acceptors]

        return JsonResponse(data, safe=False)


class PbnSitesAPIView(View):
    def get(self, request, pbn_site_id=None):
        if pbn_site_id:
            pbn_site = PbnSites.objects.using(DB).filter(id=pbn_site_id).first()
            if pbn_site:
                data = pbn_site.to_json()
            else:
                data = {}
        else:
            pbn_sites = PbnSites.objects.using(DB).all()
            data = [pbn_site.to_json() for pbn_site in pbn_sites]

        return JsonResponse(data, safe=False)


class RelationPbnSitesLinksAllDomainsAPIView(View):
    def get(self, request, relation_id=None):
        if relation_id:
            relation = RelationPbnSitesLinksAllDomains.objects.using(DB).filter(id=relation_id).first()
            if relation:
                data = relation.to_json()
            else:
                data = {}
        else:
            relations = RelationPbnSitesLinksAllDomains.objects.using(DB).all()
            data = [relation.to_json() for relation in relations]

        return JsonResponse(data, safe=False)


class MoneySitesAPIView(View):
    def get(self, request, money_site_id=None):
        if money_site_id:
            money_site = MoneySites.objects.using(DB).filter(id=money_site_id).first()
            if money_site:
                data = money_site.to_json()
            else:
                data = {}
        else:
            money_sites = MoneySites.objects.using(DB).all()
            data = [money_site.to_json() for money_site in money_sites]

        return JsonResponse(data, safe=False)


class ClientsAPIView(View):
    def get(self, request, client_id=None):
        if client_id:
            client = Clients.objects.using(DB).filter(id=client_id).first()
            if client:
                data = client.to_json()
            else:
                data = {}
        else:
            clients = Clients.objects.using(DB).all()
            data = [client.to_json() for client in clients]

        return JsonResponse(data, safe=False)


class ServersAPIView(View):
    def get(self, request, server_id=None):
        if server_id:
            server = Servers.objects.using(DB).filter(id=server_id).first()
            if server:
                data = server.to_json()
            else:
                data = {}
        else:
            servers = Servers.objects.using(DB).all()
            data = [server.to_json() for server in servers]

        return JsonResponse(data, safe=False)


class PbnArticlesAPIView(View):
    def get(self, request, article_id=None):
        if article_id:
            article = PbnArticles.objects.using(DB).filter(id=article_id).first()
            if article:
                data = article.to_json()
            else:
                data = {}
        else:
            articles = PbnArticles.objects.using(DB).all()
            data = [article.to_json() for article in articles]

        return JsonResponse(data, safe=False)


@csrf_exempt
def domain_pbn_and_publications(request, client_id):
    if request.method == 'GET':
        try:
            data = get_domain_and_pbn_publications()
            return JsonResponse(data, safe=False)
            # Return the data as JSON response
        except Exception:
            return JsonResponse({'status': 'error'})


@csrf_exempt
def get_publications_chart(request, client_id=None):
    if request.method == 'GET':
        data = get_publications_by_client(client_id)
        return JsonResponse(data, safe=False)
