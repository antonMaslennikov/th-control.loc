import json
import os
import random
import string
import time

import requests
import csv
import codecs

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Count, Q
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from project.models import Project, Invite, UsersRelation, Service, ProjectServiceSetting, Job, JobResult, Setting
from thcontrol import settings
from .forms import ProjectForm, InviteForm, RunServiceForm, RunService2Form


def getmyprojects(request):
    projects = Project.objects.filter(
        Q(author_id=request.user.id) | Q(users__id=request.user.id),
        is_deleted=False
    ).annotate(total=Count('id'))

    # print(str(projects.query))

    return projects


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


@login_required
def index(request):
    return render(request, 'project/index.html', {'projects': getmyprojects(request)})


@login_required
def detail(request, pk):
    try:
        project = Project.objects.get(
            pk=pk,
            is_deleted=False,
        )

        project_users = [];

        for user in project.users.values('id'):
            project_users.append(user['id'])

        if project.author_id != request.user.id and request.user.id not in project_users:
            raise Http404('No access')

    except Project.DoesNotExist:
        raise Http404('No access')

    return render(request, 'project/detail.html', {
        'projects': getmyprojects(request),
        'project': project,
    })


@login_required
def create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.author_id = request.user.id
            project.save()

            form.save_m2m()

            return redirect('project_detail', pk=project.id)
    else:
        form = ProjectForm()

    return render(request, 'project/create.html', {
        'projects': getmyprojects(request),
        'form': form
    })


@login_required
def update(request, pk):
    try:
        project = Project.objects.get(
            pk=pk,
            author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save(commit=False)
            project.save()

            form.save_m2m()

            return redirect('project_detail', pk=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project/create.html', {
        'projects': getmyprojects(request),
        'project': project,
        'form': form
    })


@login_required
def delete(request, pk):
    try:
        project = Project.objects.get(
            pk=pk,
            author_id=request.user.id,
            is_deleted=False
        )

        project.is_deleted = True
        project.save()

    except Project.DoesNotExist:
        raise Http404('No access')

    return redirect('index')


@login_required
def invite(request, pk):
    try:
        project = Project.objects.get(
            pk=pk,
            author_id=request.user.id,
            is_deleted=False
        )

    except Project.DoesNotExist:
        raise Http404('No access')

    if request.method == 'POST':
        form = InviteForm(request.POST, project=project)

        if form.is_valid():
            inv = form.save(commit=False)

            inv.code = generate_random_string(20)
            inv.created_by_id = request.user.id
            inv.project_id = project.id

            inv.save()

            form.send_email(inv, request)

            # set flash message
            messages.success(request, 'Инвайт был успешно отправлен на ' + inv.email)

            return redirect('project_detail', pk=project.id)
    else:
        form = InviteForm(project=project)

    return render(request, 'project/invite.html', {
        'projects': getmyprojects(request),
        'project': project,
        'form': form,
    })


def invite_accept(request, pk, code):
    try:

        invite = Invite.objects.get(
            code=code,
            accepted=0,
            project_id=pk
        )

    except Invite.DoesNotExist:
        raise Http404('The invitation is no longer available')

    # создаём нового пользователя в системе (ЕСЛИ ОН УЖЕ НЕ ЗАРЕГИСТРИРОВАН В СИСТЕМЕ)
    # и отправляем ему сгенерированные регистрационные данные на почту
    users = get_user_model()

    password = None

    try:
        user = users.objects.get(email=invite.email)
    except users.DoesNotExist:

        password = generate_random_string(10);

        user = users.objects.create_user(
            invite.email,
            invite.email,
            password,
            is_active=True,
            last_login=timezone.now()
        )

        message = render_to_string('project/invite_accepted.html', {
            'user': user,
            'password': password,
            'project': invite.project,
            'current_site': get_current_site(request)
        })

        email = EmailMessage('Invite to project accepted', message, to=[user.email])
        email.content_subtype = "html"
        email.send()

    # подключаем его к проекту
    # if password:
    UsersRelation(user=user, project=invite.project).save()

    login(request, user)

    # помечаем инвайт как использованный
    invite.accepted = True
    invite.accepted_at = timezone.datetime.now()
    invite.save()

    # set flash message
    messages.success(request, 'Инвайт был успешно принят.' + (
        ' Данные для входа отправлены на Ваш email ' + invite.email if password else ''))

    return redirect('project_detail', pk=invite.project.id)


def remove_from_project(request, pk, user_id):
    try:
        project = Project.objects.get(
            pk=pk,
            author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    try:
        users = get_user_model()
        user = users.objects.get(pk=user_id)
    except users.DoesNotExist:
        raise Http404('No access')

    project.users.remove(user)

    return redirect('project_detail', pk=project.id)


@login_required
def connect_service(request, pk, service_id=None):
    try:
        project = Project.objects.get(
            pk=pk,
            # author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    project_users = [];

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    if (service_id is None):

        if "traffic-hunters" not in request.user.email and request.user.id != 1:
            services = Service.objects.filter(
                service_class=1,
            ).all()
        else:
            services = Service.objects.all()

        return render(request, 'project/service/connect.html', {
            'projects': getmyprojects(request),
            'project': project,
            'services': services,
        })
    else:

        try:
            service = Service.objects.get(
                pk=service_id,
            )
        except Project.DoesNotExist:
            raise Http404('Service not founded')

        # service_settings_count = len(service.settings.all())

        # if request.method == 'POST' or service_settings_count == 0:
        if request.method == 'POST':

            # прикрепляем сервис к проекту
            project.services.add(service)

            # if service_settings_count > 0:
            # удаляем все предыдущие настройки
            pass_s = ProjectServiceSetting.objects.filter(
                project_id=project.id,
                service_id=service.id,
            )

            pass_s.delete()

            # myfile = request.FILES['file']
            # fs = FileSystemStorage()
            # filename = fs.save('datafiles/' + myfile.name, myfile)

            # сохраняем настройки
            for i, sid in enumerate(request.POST.getlist("setting_id")):

                Sett = Setting.objects.get(pk=sid)

                for value in request.POST.getlist("setting_value_" + sid):
                    if value:
                        ps = ProjectServiceSetting()
                        ps.project_id = project.id
                        ps.service_id = service.id
                        ps.setting_id = sid
                        ps.value = value.strip()
                        ps.save()

                # File
                if Sett.type == 2:
                    for i, sid in enumerate(request.POST.getlist("setting_id")):
                        file = request.FILES.get("setting_value_" + sid)
                        if file:
                            value = file.read().decode("utf-8")

                            if value:
                                ps = ProjectServiceSetting()
                                ps.project_id = project.id
                                ps.service_id = service.id
                                ps.setting_id = sid
                                ps.value = value.strip()
                                ps.save()

            messages.success(request, 'Сервис ' + service.name + ' успешно подключен')

            return redirect('project_detail', pk=project.id)
        else:

            ProjectServiceSettings = ProjectServiceSetting.objects.filter(
                project_id=project.id,
                service_id=service.id,
            )

            settings = {}

            for setting in ProjectServiceSettings:
                if not settings.get(setting.setting_id):
                    settings[setting.setting_id] = []

                settings[setting.setting_id].append(setting.value)

            # ищем или создаём (при первом запуске приложения) общую настройку "урл запуска"
            try:
                S = Setting.objects.get(key=Setting.SERVICE_URL_NAME)
            except Setting.DoesNotExist:
                S = Setting()
                S.key = Setting.SERVICE_URL_NAME
                S.description = 'Url для запуска сервиса (НЕ УДАЛЯТЬ!!!)'
                S.save()

        return render(request, 'project/service/pre_settings.html', {
            'projects': getmyprojects(request),
            'project': project,
            'service': service,
            'settings': settings,
            'url_setting': S,
        })


@login_required
def disconnect_service(request, pk, service_id):
    try:
        project = Project.objects.get(
            pk=pk,
            author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')

    project.services.remove(service)

    return redirect('project_connect_service', pk=pk)

    pass


def run_service(request, pk, service_id):
    project = Project.objects.get(
        pk=pk,
        is_deleted=False,
    )

    project_users = []

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')

    if request.method == 'POST':

        if service.service_class == 2:
            form = RunService2Form(request.POST, request.FILES)
        else:
            form = RunServiceForm(request.POST, request.FILES)

        if form.is_valid():

            fs = FileSystemStorage()

            if service.service_class == 2:
                data = []
                folder = 'datafiles/' + str(time.time_ns()) + '/'
                os.makedirs(folder)
                for f in request.FILES.getlist('file'):
                    filename = fs.save(folder + f.name, f)
                    # data.append(fs.url(filename))
                    data.append(settings.MEDIA_URL + filename)

                data = json.dumps(data)
            else:
                f = request.FILES['file']
                filename = fs.save('datafiles/' + f.name, f)
                data = settings.MEDIA_URL + filename

            J = Job()
            J.status = 0
            J.project_id = project.id
            J.service_id = service.id
            J.data = data
            J.save()

            # отправка запроса внешнему сервису на запуск
            service_url = ProjectServiceSetting.getone(project.id, service.id, Setting.SERVICE_URL_NAME)
            if service_url:
                response = requests.get(
                    service_url.rstrip('/') + reverse('project_job_run', args=(project.id, service.id,)))

            messages.success(request, 'Сервис ' + service.name + ' успешно запущен.')

            return redirect('project_service_journal', pk=project.id, service_id=service.id)
    else:
        if service.service_class == 2:
            form = RunService2Form()
        else:
            form = RunServiceForm()

    return render(request, 'project/service/run.html', {
        'projects': getmyprojects(request),
        'project': project,
        'service': service,
        'form': form,
    })


def restart_service(request, pk, service_id, job_id):
    project = Project.objects.get(
        pk=pk,
        is_deleted=False,
    )

    project_users = []

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')

    job = Job.objects.get(pk=job_id)
    job.status = 0
    job.save()

    return redirect('project_service_journal', pk=project.id, service_id=service_id)


def journal_service(request, pk, service_id):
    try:
        project = Project.objects.get(
            pk=pk,
            # author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    project_users = []

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')


    jobs = Job.objects.filter(
        project_id=project.id,
        service_id=service.id,
    ).order_by('-id')

    tpl = 'project/service/journal.html'
    results = None

    return render(request, tpl, {
        'projects': getmyprojects(request),
        'project': project,
        'service': service,
        'jobs': jobs,
        'results': results,
    })


def service_log(request, pk, service_id, job_id=None, download=None):
    try:
        project = Project.objects.get(
            pk=pk,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    project_users = []

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')

    if download:
        limit = 500000
    else:
        limit = 100

    if job_id is None:
        jobs = list(Job.objects\
                    .filter(
                        project_id=project.id,
                        service_id=service.id
                    )\
                    .order_by('-id')\
                    .values_list('id', flat=True)\
                    .all()[:limit])
    else:
        jobs = Job.objects.filter(pk=job_id)
        pass

    results = JobResult.objects.filter(job_id__in=jobs).order_by('-id')

    if 'search' in request.GET:
        results = results.filter(result__contains=request.GET['search'])

    # print(results.query)

    log = []

    for row in results:
        if row.result_data:
            log_row = json.loads(row.result_data)

            if type(log_row) == list:
                for l in log_row:

                    keys = l.keys()

                    for k in keys:
                        l[k] = l[k].rstrip("\n")

                    if 'search' in request.GET:
                        for k in keys:
                            if request.GET['search'] in l[k]:
                                log.append(l)
                    else:
                        log.append(l)

                    if len(log) >= 500 and not job_id and not download:
                        break
            else:
                keys = log_row.keys()

                for k in keys:
                    log_row[k] = log_row[k].rstrip("\n")

                if 'search' in request.GET:
                    for k in keys:
                        if request.GET['search'] in log_row[k]:
                            log.append(log_row)
                else:
                    log.append(log_row)

                if len(log) >= 500 and not job_id and not download:
                    break


        if len(log) >= 500 and not job_id and not download:
            break


    if download:
        keys = log[0].keys()

        # if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'downloads')):
        #     os.mkdir(os.path.join(settings.MEDIA_ROOT, 'downloads'))
        #
        # file_location = os.path.join(settings.MEDIA_ROOT, 'downloads/' + str(random.randint(1, 10000)) + '.csv')

        # with open(file_location, 'w', encoding='utf-8', newline='') as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(log)

        try:
            # with open(file_location, 'r') as f:
            #     file_data = f.read()

            # response = HttpResponse(file_data, content_type='text/csv; charset=windows-1251')
            # response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(file_location) + '"'

            response = HttpResponse(content_type='text/csv')

            response['Content-Disposition'] = 'attachment; filename="' + str(random.randint(1, 10000)) + '.csv"'

            response.write(codecs.BOM_UTF8)

            dict_writer = csv.DictWriter(response, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(log)

        except IOError:
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response

    print(log)

    return render(request, 'project/service/log.html', {
        'project': project,
        'service': service,
        'job_id': job_id,
        'results': log,
        'projects': getmyprojects(request),
    })


def jobinfo(request, job_id):
    try:
        job = Job.objects.get(
            pk=job_id,
        )
    except Job.DoesNotExist:
        raise Http404('No access')

    if job.project.secret_key and job.project.secret_key != request.headers.get('authorization'):
        raise Http404('No access: ключ авторизации не указан')

    try:
        ProjectServiceSettings = ProjectServiceSetting.objects.filter(
            project_id=job.project.id,
            service_id=job.service.id,
        )

        settings = []

        for pss in ProjectServiceSettings.all():
            settings.append({
                'key': pss.setting.key,
                'value': pss.value,
            })

    except ProjectServiceSetting.DoesNotExist:
        raise Http404('No access')

    return JsonResponse({
        'job_id': job.id,
        'data': job.data,
        'service': {
            'id': job.service.id,
            'name': job.service.name,
            'settings': settings,
        },
        'project': {
            'id': job.project.id,
            'name': job.project.name,
        },
    })


@require_http_methods(["POST"])
def jobresult(request, job_id):
    try:
        job = Job.objects.get(
            pk=job_id,
        )
    except Job.DoesNotExist:
        raise Http404('No access')

    if job.project.secret_key and job.project.secret_key != request.headers.get('authorization'):
        raise Http404('No access: ключ авторизации не указан')

    R = JobResult
    R.job_id = job_id
    R.result = request.POST.result
    R.save()

    if request.POST.status in [2, 3, 4]:
        job.status = request.POST.status

        if request.POST.status == 2:
            job.finished_at = timezone.datetime.now()

        job.save()

    return JsonResponse({
        'status': 'ok'
    })


def jobrun(request, project_id, job_id):
    # print(project_id, job_id)

    return JsonResponse({
        'status': 'ok'
    })


@login_required
def connect_crm(request):
    try:

        print('hola')

    except Project.DoesNotExist:
        raise Http404('No access')

    return render(request, 'project/connect_crm.html', {
        'projects': getmyprojects(request),
        # 'form': form
    })
