from django.urls import path, re_path
 
# from .views import SignUpView;
from . import views
 
urlpatterns = [
    path('signup/', views.singup, name='signup'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'), 
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate')
]