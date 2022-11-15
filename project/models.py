from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

# --------------------------------------------------------------------------------------------------

class Type(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

# --------------------------------------------------------------------------------------------------

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# --------------------------------------------------------------------------------------------------

class Project(models.Model):

    name = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_id')
    url = models.CharField(max_length=255)
    is_service = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UsersRelation')
    regions = models.ManyToManyField(Region)
    types = models.ManyToManyField(Type)

    def __str__(self):
        return self.name


# --------------------------------------------------------------------------------------------------

class UsersRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
