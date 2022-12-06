from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='project_detail'),
    path('create/', views.create, name='project_create'),
    path('update/<int:pk>/', views.update, name='project_update'),
    path('delete/<int:pk>/', views.delete, name='project_delete'),
    path('invite/<int:pk>/', views.invite, name='project_invite'),
    path('connect_crm/', views.connect_crm, name='project_connect_crm'),
]