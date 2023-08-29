from django.shortcuts import render
from .queries import query_get_clients_list, query_get_money_sites_list, query_get_deadline_data, query_get_new_domains, \
    query_get_chart_data, query_get_new_publications, query_get_new_pbn_domains, query_get_links_to_money_sites, \
    query_get_pbn_domains, query_links_to_money_sites, query_anchor_links
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'lookerstudio/index.html')


def get_client_list(request):
    data = query_get_clients_list()
    return JsonResponse(data, safe=False)


def get_money_sites_list(request):
    clients = request.GET.get('clients', None)
    data = query_get_money_sites_list(clients)
    return JsonResponse(data, safe=False)


def get_deadline_data(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_get_deadline_data(clients, money_sites)
    return JsonResponse(data, safe=False)


def get_summary(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    data = {'new_domains': query_get_new_domains(clients, money_sites, start_date, end_date),
            'publications': query_get_new_publications(clients, money_sites),
            'pbn_domains': query_get_new_pbn_domains(clients, money_sites),
            'money_sites': query_get_links_to_money_sites(clients, money_sites)}
    return JsonResponse(data, safe=False)


def get_chart_date(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_get_chart_data(clients, money_sites)
    return JsonResponse(data, safe=False)


def get_pbn_domains_and_publications(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_get_pbn_domains(clients, money_sites)
    data = paginator_prepare(data, 1)
    return JsonResponse(data, safe=False)


def get_links_to_money_sites(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_links_to_money_sites(clients, money_sites)
    data = paginator_prepare(data, 1)
    return JsonResponse(data, safe=False)


def get_anchor_links(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_anchor_links(clients, money_sites, 1)
    data = paginator_prepare(data, 1)
    return JsonResponse(data, safe=False)


def paginator_prepare(page, page_number=1):
    links = []
    for link in page.object_list:
        links.append(link)
    return {
        'links': links,
        'page_number': page_number,
        'total_pages': page.paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
    }
