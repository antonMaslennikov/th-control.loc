from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='project_detail'),
    path('create/', views.create, name='project_create'),
    path('update/<int:pk>/', views.update, name='project_update'),
    path('delete/<int:pk>/', views.delete, name='project_delete'),
    path('invite/<int:pk>/', views.invite, name='project_invite'),
    path('invite/<int:pk>/accept/<str:code>', views.invite_accept, name='project_invite_accept'),
    path('remove_from_project/<int:pk>/<int:user_id>', views.remove_from_project, name='remove_from_project'),
    path('connect_service/<int:pk>/', views.connect_service, name='project_connect_service'),
    path('connect_service/<int:pk>/<int:service_id>', views.connect_service, name='project_connect_service'),
    path('disconnect_service/<int:pk>/<int:service_id>', views.disconnect_service, name='project_disconnect_service'),
    path('run_service/<int:pk>/<int:service_id>', views.run_service, name='project_run_service'),
    path('service_settings/<int:pk>/<int:service_id>', views.service_settings, name='project_service_settings'),
    path('journal_service/<int:pk>/<int:service_id>', views.journal_service, name='project_service_journal'),
    path('journal_service/<int:pk>/<int:service_id>/<int:job_id>', views.journal_service, name='project_service_job_journal'),
    path('jobinfo/<int:job_id>', views.jobinfo),
    path('jobresult/<int:job_id>', views.jobresult),

    path('connect_crm/', views.connect_crm, name='project_connect_crm'),
]