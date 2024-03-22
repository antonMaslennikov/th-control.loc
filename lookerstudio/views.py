from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .queries import query_get_clients_list, query_get_money_sites_list, query_get_deadline_data, query_get_new_domains, \
    query_get_chart_data, query_get_new_publications, query_get_new_pbn_domains, query_get_links_to_money_sites, \
    query_get_pbn_domains, query_links_to_money_sites, query_anchor_links, query_summary, query_get_publications, \
    query_get_chart_redirects_data, get_paginator
from django.http import JsonResponse


# Create your views here.
@login_required
def index(request):
    return render(request, 'lookerstudio/index.html')

@login_required
def summary(request):
    return render(request, 'lookerstudio/summary.html')

@login_required
def expireds(request):
    sql_query = 'SELECT c.client_name, ' \
                '   ps.site_url, ' \
                '   ps.registration_expiration, ' \
                '   DATEDIFF(registration_expiration, CURRENT_DATE()) AS registration_expiration_rest, ' \
                '   ps.ssl_expiration,' \
                '   DATEDIFF(ssl_expiration, CURRENT_DATE()) AS ssl_expiration_rest ' \
                'FROM pbn_sites ps ' \
                '   JOIN servers s ON ps.id_server = s.id ' \
                '   JOIN clients c ON s.client_id = c.id ' \
                'WHERE ' \
                '   ps.registration_expiration IS NOT NULL ' \
                'ORDER BY ' \
                '   IF (registration_expiration IS NULL || registration_expiration = \'0000-00-00\', 0, 1) DESC, ' \
                '   registration_expiration, ' \
                '   ssl_expiration'

    page = get_paginator(sql_query, '', request.GET.get('page', 1), request.GET.get('per_page', 20))

    return render(request, 'lookerstudio/expireds.html', {
        'paginator': page,
        'min_page': max(1, page.number - 5),
        'max_page': min(page.paginator.num_pages, page.number + 5),
    })


def summary_page_data(request):
    data = query_summary()
    return JsonResponse(data, safe=False)


def get_client_list(request):
    data = query_get_clients_list()
    return JsonResponse(data, safe=False)


def get_money_sites_list(request):
    clients = request.GET.get('clients', None)
    data = query_get_money_sites_list(clients)
    return JsonResponse(data, safe=False)

def get_publications(request):
    clients = request.GET.get('clients', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('per_page', 5)
    data = query_get_publications(clients, start_date, end_date, page_number, items_per_page)
    data = paginator_prepare(data, page_number)
    return JsonResponse(data, safe=False)

def get_deadline_data(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_get_deadline_data(clients)
    return JsonResponse(data, safe=False)


def get_summary(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    data = {
        'pbn_domains': query_get_new_pbn_domains(clients, money_sites),
        'new_domains': query_get_new_domains(clients, start_date, end_date),

        'publications': query_get_new_publications(clients),
        'new_publications': query_get_new_publications(clients, start_date, end_date),

        'money_sites': query_get_links_to_money_sites(clients, money_sites),

        'deadline_data': query_get_deadline_data(clients),
    }
    return JsonResponse(data, safe=False)


def get_chart_date(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    data = query_get_chart_data(clients, money_sites)
    return JsonResponse(data, safe=False)
def get_chart_redirects_data(request):

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)

    data = query_get_chart_redirects_data(start_date, end_date, clients, money_sites)
    return JsonResponse(data, safe=False)


def get_pbn_domains_and_publications(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('per_page', 5)
    data = query_get_pbn_domains(clients, money_sites, start_date, end_date, page_number, items_per_page)
    data = paginator_prepare(data, page_number)
    return JsonResponse(data, safe=False)


def get_links_to_money_sites(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('per_page', 5)
    data = query_links_to_money_sites(clients, money_sites, page_number, items_per_page)
    data = paginator_prepare(data, page_number)
    return JsonResponse(data, safe=False)


def get_anchor_links(request):
    clients = request.GET.get('clients', None)
    money_sites = request.GET.get('money_sites', None)
    query_type = request.GET.get('query_type', 1)
    data = query_anchor_links(clients, money_sites, query_type=query_type)
    data = paginator_prepare(data)
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
