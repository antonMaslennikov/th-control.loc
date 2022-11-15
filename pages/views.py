from django.shortcuts import render
from project.models import Project

def index(request):
    projects = Project.objects.all()
    return render(request, 'pages/index.html', {'projects': projects})
    