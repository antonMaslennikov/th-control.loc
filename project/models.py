from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

# ----------------------------------------------------------------------------------------------------------------------

class Type(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

# ----------------------------------------------------------------------------------------------------------------------


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------------------------------------------------
class Setting(models.Model):
    key = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.key + ' (' + self.description + ')'

# ----------------------------------------------------------------------------------------------------------------------
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    settings = models.ManyToManyField(Setting)

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------------------------------------------------
class Project(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_id')
    url = models.CharField(max_length=255)
    is_service = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UsersRelation')
    regions = models.ManyToManyField(Region, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    types = models.ManyToManyField(Type, blank=True)
    is_deleted = models.BooleanField(default=0)
    secret_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# ----------------------------------------------------------------------------------------------------------------------


class UsersRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


# ----------------------------------------------------------------------------------------------------------------------
class Invite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    code = models.CharField(max_length=30)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=0)
    accepted_at = models.DateTimeField(blank=True, null=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_user', blank=True, null=True)


# ----------------------------------------------------------------------------------------------------------------------
class ProjectServiceSetting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'service', 'setting',)


# ----------------------------------------------------------------------------------------------------------------------
class Job(models.Model):
    STATUS = (
        (1, '??????????????'),
        (2, '?????????????? ????????????????'),
        (3, '???????????????????? ??????????????'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    data = models.TextField()
    status = models.IntegerField(choices=STATUS, default=1)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    finished_at = models.DateTimeField(blank=True, null=True)


# ----------------------------------------------------------------------------------------------------------------------
class JobResult(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)