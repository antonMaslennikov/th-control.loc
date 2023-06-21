from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Clients, LinksAllAnchors, LinksAllDomains, LinksAllUrls, LinksCheckDonorAcceptor, MoneySites, PbnArticles, PbnSites, RelationPbnSitesLinksAllDomains, Servers

def serialize_model(model_instances):
    serialized_data = serialize('json', model_instances)
    deserialized_data = JsonResponse(serialized_data, safe=False)
    return deserialized_data
