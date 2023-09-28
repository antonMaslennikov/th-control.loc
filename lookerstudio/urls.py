from django.urls import path

from .views import (
    index, summary, get_client_list, get_money_sites_list, get_deadline_data, get_summary, get_chart_date,
    get_pbn_domains_and_publications, get_links_to_money_sites, get_anchor_links, summary_page_data
)

urlpatterns = [
    path('', index),
    path('summary', summary),
    path('summary_page_data', summary_page_data),
    path('get-client-list', get_client_list),
    path('get-money-sites-list', get_money_sites_list),
    path('get-deadline-data', get_deadline_data),
    path('get-summary', get_summary),
    path('chart-data', get_chart_date),
    path('domain-and-publications', get_pbn_domains_and_publications),
    path('link-to-money-sites', get_links_to_money_sites),
    path('anchor-links', get_anchor_links),
]
