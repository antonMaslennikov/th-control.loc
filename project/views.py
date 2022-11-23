from django.shortcuts import render
from project.models import Project
from django.contrib.auth.decorators import login_required

def getmyprojects():
    projects = projects = Project.objects.all()
    return projects

@login_required
def index(request):
    return render(request, 'project/index.html', {'projects': getmyprojects})

@login_required
def detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'project/detail.html', {'projects': getmyprojects, 'project': project,})

@login_required
def create(request):
    return render(request, 'project/create.html', {'projects': getmyprojects})
