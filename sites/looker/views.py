from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .queries import get_count_new_domains, get_count_new_publications, get_count_publications, get_chart_data, \
    get_money_sites_lists, \
    get_client_list, get_domain_pbn_and_publications, get_links_to_money_sites, get_anchor_lists
import services.Service

from django.http import JsonResponse
from django.views import View
from .models import (
    LinksAllDomains, LinksAllUrls, LinksCheckDonorAcceptor, PbnSites,
    RelationPbnSitesLinksAllDomains, MoneySites, PbnArticles, Servers, Clients,
)
from .settings import DB
from django.db.models import Count, Max, DurationField, ExpressionWrapper, IntegerField, F
from django.utils.timezone import now


def index(request):
    return render(request, 'looker/index.html')


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


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ---
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class SummaryAPIView(View):
    def get(self, request):
        client_id = request.GET.get('client_id', None)
        money_sites_id = request.GET.get('money_sites_id', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        data = {}
        data['count_new_domains'] = get_count_new_domains(client_id=client_id, money_sites=money_sites_id,
                                                          start_date=start_date,
                                                          end_date=end_date)

        data['count_publications'] = get_count_publications(client_id=client_id, money_sites=money_sites_id)

        data['count_new_publications'] = get_count_new_publications(client_id=client_id, money_sites=money_sites_id,
                                                                    start_date=start_date,
                                                                    end_date=end_date)

        return JsonResponse(data, safe=False)


class ChartDataAPIView(View):
    def get(self, request):
        client_id = request.GET.get('client_id', None)
        money_sites_id = request.GET.get('money_sites_id', None)
        data = get_chart_data(client_id, money_sites_id)
        return JsonResponse(data, safe=False)


class FiltersAPIView(View):
    def get(self, request):
        client_id = request.GET.get('client_id', None)
        money_sites_id = request.GET.get('money_sites_id', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        data = {'client_list': get_client_list(), 'money_sites': get_money_sites_lists(client_id)}
        return JsonResponse(data, safe=False)


class TableDomainAndPublicationsAPIView(View):
    def get(self, request):
        if request.method == 'GET':
            try:
                page_number = request.GET.get('page', 1)
                items_per_page = request.GET.get('per_page', 5)
                client_id = request.GET.get('client_id', None)
                money_sites = request.GET.get('money_sites', None)
                page = get_domain_pbn_and_publications(client_id=client_id, current_page=page_number,
                                                       items_per_page=items_per_page, money_sites=money_sites)
                links = []
                for link in page.object_list:
                    link_dict = {
                        'client_name': link[0],
                        'pbn_domain': link[1],
                        'date_create': link[2],
                        'total_publications': link[3],
                        'last_post': link[4],
                        'day_since_last_publication': link[5],
                    }
                    links.append(link_dict)
                response = {
                    'links': links,
                    'page_number': page_number,
                    'total_pages': page.paginator.num_pages,
                    'has_previous': page.has_previous(),
                    'has_next': page.has_next(),
                }
                return JsonResponse(response, safe=False)
                # Return the data as JSON response
            except Exception:
                return JsonResponse({'status': 'error'})


class TableLinksToMoneySitesAPIView(View):
    def get(self, request):
        if request.method == 'GET':
            try:
                page_number = request.GET.get('page', 1)
                items_per_page = request.GET.get('per_page', 10)
                client_id = request.GET.get('client_id', None)
                money_sites = request.GET.get('money_sites', None)
                page = get_links_to_money_sites(current_page=page_number, items_per_page=items_per_page,
                                                client_id=client_id, money_sites=money_sites)
                links = []
                for link in page.object_list:
                    link_dict = {
                        'url_from_donor': link[0],
                        'anchor_value': link[1],
                        'url_to_acceptor': link[2]
                    }
                    links.append(link_dict)
                response = {
                    'links': links,
                    'page_number': page_number,
                    'total_pages': page.paginator.num_pages,
                    'has_previous': page.has_previous(),
                    'has_next': page.has_next(),
                }
                return JsonResponse(response, safe=False)
                # Return the data as JSON response
            except Exception:
                return JsonResponse({'status': 'error'})


class TableAnchorsAPIView(View):
    def get(self, request):
        if request.method == 'GET':
            try:
                page_number = request.GET.get('page', 1)
                items_per_page = request.GET.get('per_page', 5)
                stage = int(request.GET.get('stage', 1))
                client_id = request.GET.get('client_id', None)
                money_sites = request.GET.get('money_sites', None)
                print(client_id)
                page = get_anchor_lists(current_page=page_number, items_per_page=items_per_page, stage=stage,
                                        client_id=client_id, money_sites=money_sites)
                links = []
                for link in page.object_list:
                    if stage == 0:
                        link_dict = {
                            'anchor_value': link[0],
                            'url_count': link[1]
                        }
                    else:
                        link_dict = {
                            'anchor_value': link[0],
                            'accepted_domain': link[1],
                            'url_count': link[2]
                        }
                    links.append(link_dict)
                response = {
                    'links': links,
                    'total_pages': page.paginator.num_pages,
                    'page_number': page_number,
                    'has_previous': page.has_previous(),
                    'has_next': page.has_next(),
                }
                return JsonResponse(response, safe=False)
                # Return the data as JSON response
            except Exception:
                return JsonResponse({'status': 'error'})
