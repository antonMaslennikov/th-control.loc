from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .service import get_domain_and_pbn_publications, get_publications_by_client
from . import models
from .serializers import serialize
from .models import Clients, LinksAllAnchors, Servers
from .settings import DB


def index(request):
    return render(request, 'looker/index.html')


@csrf_exempt
def clients_list(request):
    if request.method == 'GET':
        clients = Clients.objects.using(DB).all()
        data = [{'id': client.pk, 'client_name': client.client_name, 'date_add': client.date_add} for client in
                clients]
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
def get_publications_chart(request):
    if request.method == 'GET':
        data = get_publications_by_client()
        return JsonResponse(data, safe=False)


@csrf_exempt
def links_anchor(request, id):
    if request.method == 'GET':
        anchors = LinksAllAnchors.objects.using(DB).all()
        data = [{'anchor_value': anchor.anchor_value, 'date_add': anchor.date_add} for anchor in anchors]
        return JsonResponse(data, safe=False)
