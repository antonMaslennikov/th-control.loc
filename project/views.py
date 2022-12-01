from django.shortcuts import render, redirect
from project.models import Project
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import ProjectForm

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

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        
        if form.is_valid():

            project = form.save(commit=False)
            project.author_id = request.user.id
            project.save()

            form.save_m2m()

            return redirect('project_detail', pk=project.id)
    else:
        form = ProjectForm()

    return render(request, 'project/create.html', {
        'projects': getmyprojects(request),
        'form': form
        })


@login_required
def update(request, pk):

    try:
        project = Project.objects.get(
            pk=pk, 
            author_id = request.user.id,
            is_deleted = False
            )
    except Project.DoesNotExist:
        raise Http404('No access')  


    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        
        if form.is_valid():

            project = form.save(commit=False)
            project.save()

            form.save_m2m()

            return redirect('project_detail', pk=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project/create.html', {
        'projects': getmyprojects(request),
        'form': form
        })
