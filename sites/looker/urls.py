from django.urls import path
from .views import (
    LinksAllDomainsAPIView, LinksAllUrlsAPIView, LinksCheckDonorAcceptorAPIView,
    PbnSitesAPIView, RelationPbnSitesLinksAllDomainsAPIView, MoneySitesAPIView,
    PbnArticlesAPIView, get_publications_chart, domain_pbn_and_publications
)

app_name = 'looker'

urlpatterns = [
    path('api/links-all-domains/', LinksAllDomainsAPIView.as_view(), name='links_all_domains_api'),
    path('api/links-all-domains/<int:domain_id>/', LinksAllDomainsAPIView.as_view(),
         name='links_all_domains_detail_api'),
    path('api/links-all-urls/', LinksAllUrlsAPIView.as_view(), name='links_all_urls_api'),
    path('api/links-all-urls/<int:url_id>/', LinksAllUrlsAPIView.as_view(), name='links_all_urls_detail_api'),
    path('api/links-check-donor-acceptor/', LinksCheckDonorAcceptorAPIView.as_view(),
         name='links_check_donor_acceptor_api'),
    path('api/links-check-donor-acceptor/<int:donor_acceptor_id>/', LinksCheckDonorAcceptorAPIView.as_view(),
         name='links_check_donor_acceptor_detail_api'),
    path('api/pbn-sites/', PbnSitesAPIView.as_view(), name='pbn_sites_api'),
    path('api/pbn-sites/<int:pbn_site_id>/', PbnSitesAPIView.as_view(), name='pbn_sites_detail_api'),
    path('api/relation-pbn-sites-links-all-domains/', RelationPbnSitesLinksAllDomainsAPIView.as_view(),
         name='relation_pbn_sites_links_all_domains_api'),
    path('api/relation-pbn-sites-links-all-domains/<int:relation_id>/',
         RelationPbnSitesLinksAllDomainsAPIView.as_view(), name='relation_pbn_sites_links_all_domains_detail_api'),
    path('api/money-sites/', MoneySitesAPIView.as_view(), name='money_sites_api'),
    path('api/money-sites/<int:money_site_id>/', MoneySitesAPIView.as_view(), name='money_sites_detail_api'),
    path('api/pbn-articles/', PbnArticlesAPIView.as_view(), name='pbn_articles_api'),
    path('api/pbn-articles/<int:article_id>/', PbnArticlesAPIView.as_view(), name='pbn_articles_detail_api'),
    path('api/get-publications-chart', get_publications_chart),
    path('api/domain-pbn-and-publications', domain_pbn_and_publications),
]
