from django.contrib import admin

# Register your models here.
from .models import Project, Type, Region

admin.site.register(Project)
admin.site.register(Type)
admin.site.register(Region)
