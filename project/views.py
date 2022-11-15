from django.shortcuts import render
from project.models import Project

def index(request):
    projects = Project.objects.all()
    return render(request, 'project/index.html', {'projects': projects})

def detail(request, pk):
    # projects = Project.objects.all()
    project = Project.objects.get(pk=pk)
    return render(request, 'project/detail.html', {'project': project})
