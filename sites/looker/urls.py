from django.urls import path
from .views import get_publications_chart, domain_pbn_and_publications, index, clients_list

app_name = 'looker'
urlpatterns = [
    path('', index),
    path('api/clients', clients_list),
    path('api/get-publications-chart', get_publications_chart),
    path('api/domain-pbn-and-publications', domain_pbn_and_publications),

]
