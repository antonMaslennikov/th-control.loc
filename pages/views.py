from django.shortcuts import render
from project.models import Project

def index(request):
    return render(request, 'pages/index.html', {})

    