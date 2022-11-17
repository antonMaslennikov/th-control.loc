from django.shortcuts import render
from project.models import Project
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    projects = Project.objects.all()
    return render(request, 'project/index.html', {'projects': projects})

@login_required
def detail(request, pk):
    # projects = Project.objects.all()
    project = Project.objects.get(pk=pk)
    return render(request, 'project/detail.html', {'project': project})
