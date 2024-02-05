from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='project_detail'),
    path('create', views.create, name='project_create'),
    path('<int:pk>/update', views.update, name='project_update'),
    path('<int:pk>/delete', views.delete, name='project_delete'),
    path('<int:pk>/invite', views.invite, name='project_invite'),
    path('<int:pk>/invite/accept/<str:code>', views.invite_accept, name='project_invite_accept'),
    path('<int:pk>/remove_from_project/<int:user_id>', views.remove_from_project, name='remove_from_project'),
    path('<int:pk>/connect_service', views.connect_service, name='project_connect_service'),
    path('<int:pk>/connect_service/<int:service_id>', views.connect_service, name='project_connect_service'),
    path('<int:pk>/disconnect_service/<int:service_id>', views.disconnect_service, name='project_disconnect_service'),
    path('<int:pk>/run_service/<int:service_id>', views.run_service, name='project_run_service'),
    path('<int:pk>/journal_service/<int:service_id>', views.journal_service, name='project_service_journal'),
    path('<int:pk>/log/<int:service_id>', views.service_log, name='project_service_jobs_log'),
    path('<int:pk>/log/<int:service_id>/<int:job_id>', views.service_log, name='project_service_job_journal'),
    path('<int:pk>/log/<int:service_id>/<str:download>', views.service_log, name='project_service_jobs_log_download'),
    path('<int:pk>/log/<int:service_id>/<int:job_id>/<str:download>', views.service_log, name='project_service_jobs_log_download'),
    path('<int:pk>/restart/<int:service_id>/<int:job_id>', views.restart_service, name='project_service_restart'),

    path('job/info/<int:job_id>', views.jobinfo, name='project_job_info'),
    path('job/result/<int:job_id>', views.jobresult, name='project_job_result'),
    path('job/run/<int:project_id>/<int:job_id>/', views.jobrun, name='project_job_run'),

    path('connect_crm/', views.connect_crm, name='project_connect_crm'),
]