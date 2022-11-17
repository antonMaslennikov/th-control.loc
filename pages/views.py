from django.shortcuts import render
from project.models import Project

def index(request):
    return render(request, 'pages/index.html', {})

# def login(request):
    # return render(request, 'pages/login.html', {})
    
def registration(request):
    return render(request, 'pages/registration.html', {})
    