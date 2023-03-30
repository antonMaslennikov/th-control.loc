import datetime

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
    SERVICE_URL_NAME = 'system_service_url'

    TYPES = (
        (1, 'Text'),
        (2, 'File'),
    )

    key = models.CharField(max_length=50)
    type = models.IntegerField(choices=TYPES, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.key + ' (' + str(self.description) + ')'


# ----------------------------------------------------------------------------------------------------------------------
class Service(models.Model):
    STATUS = (
        (1, 'GoogleIndexer'),
        (2, 'AhrefsAnalysis'),
    )

    name = models.CharField(max_length=255)
    service_class = models.IntegerField(choices=STATUS, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    settings = models.ManyToManyField(Setting, blank=True)

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

    # class Meta:
    #     unique_together = ('project', 'service', 'setting',)

    @staticmethod
    def getall(project_id, service_id):
        ProjectServiceSettings = ProjectServiceSetting.objects.filter(
            project_id=project_id,
            service_id=service_id,
        )

        settings = {}

        for pss in ProjectServiceSettings.all():

            if not settings.get(pss.setting.key):
                settings[pss.setting.key] = []

            settings[pss.setting.key].append(pss.value)

        return settings

    @staticmethod
    def getone(project_id, service_id, key):
        ProjectServiceSettings = ProjectServiceSetting.objects.filter(
            project_id=project_id,
            service_id=service_id,
        )

        for pss in ProjectServiceSettings.all():
            if pss.setting.key == key:
                return pss.value


# ----------------------------------------------------------------------------------------------------------------------
class Job(models.Model):
    STATUS = (
        (0, 'Ожидает запуска'),
        (1, 'Запущен'),
        (2, 'Успешно завершён'),
        (3, 'Завершился ошибкой'),
        (4, 'Промежуточный результат'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    data = models.TextField()
    status = models.IntegerField(choices=STATUS, default=1)
    delayed_at = models.DateTimeField(blank=True, null=True)
    last_repeat = models.DateTimeField(blank=True, null=True)
    last_result = models.TextField(blank=True, null=True)
    repeats = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def start(self):
        self.status = 1
        self.save()

    def intermediate(self, date=None, message=None):

        if date is None:
            now = datetime.datetime.now(tz=timezone.utc)
            currentH = int(datetime.datetime.now(tz=timezone.utc).strftime('%H'))
            # на 8 утра следующего дня
            # date = now + datetime.timedelta(hours=24 - currentH + 8)
            # на тот же час следующего дня
            date = now + datetime.timedelta(hours=24)

        self.status = 4
        self.last_result = message

        if date:
            self.delayed_at = date.strftime('%Y-%m-%d %H:%M:%S')

        self.save()

    def finish(self, success=True, message=None):
        if success:
            self.status = 2
        else:
            self.status = 3
        self.last_result = message
        self.save()

    def error(self, message=None):
        self.status = 3
        self.last_result = message
        self.save()


# ----------------------------------------------------------------------------------------------------------------------
class JobResult(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    result = models.TextField(blank=True, null=True)
    result_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)