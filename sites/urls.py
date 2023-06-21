from django.urls import path, include

urlpatterns = [
    path('looker/', include('sites.looker.urls')),
]
