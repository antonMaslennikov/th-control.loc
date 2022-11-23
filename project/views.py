from django.shortcuts import render
from project.models import Project
from django.contrib.auth.decorators import login_required
from django.http import Http404

def getmyprojects(request):
    
    projects = Project.objects.filter(
        author_id = request.user.id,
        is_deleted = False
        ) 
        # | Project.objects.filter(author_id = 2)

    # print(str(projects.query))

    return projects

@login_required
def index(request):
    return render(request, 'project/index.html', {'projects': getmyprojects(request)})

@login_required
def detail(request, pk):
    try:
        project = Project.objects.get(
            pk=pk, 
            author_id = request.user.id,
            is_deleted = False
            )
    except Project.DoesNotExist:
        raise Http404('No access')  

    return render(request, 'project/detail.html', {
        'projects': getmyprojects(request), 
        'project': project,
        })

@login_required
def create(request):
    return render(request, 'project/create.html', {'projects': getmyprojects(request)})
