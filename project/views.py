import random
import string

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Count, Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from project.models import Project, Invite, UsersRelation, Service, ProjectServiceSetting, Job, JobResult
from .forms import ProjectForm, InviteForm, RunServiceForm


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
            messages.success(request, '???????????? ?????? ?????????????? ?????????????????? ???? ' + inv.email)

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

    # ?????????????? ???????????? ???????????????????????? ?? ?????????????? (???????? ???? ?????? ???? ?????????????????????????????? ?? ??????????????)
    # ?? ???????????????????? ?????? ?????????????????????????????? ?????????????????????????????? ???????????? ???? ??????????
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


    # ???????????????????? ?????? ?? ??????????????
    if (password):
        UsersRelation(user=user, project=invite.project).save()

    login(request, user)

    # ???????????????? ???????????? ?????? ????????????????????????????
    invite.accepted = True
    invite.accepted_at = timezone.datetime.now()
    invite.save()

    # set flash message
    messages.success(request, '???????????? ?????? ?????????????? ????????????.' + (' ???????????? ?????? ?????????? ???????????????????? ???? ?????? email ' + invite.email if password else ''))

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
            author_id=request.user.id,
            is_deleted=False
        )
    except Project.DoesNotExist:
        raise Http404('No access')

    if (service_id is None):
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
            raise Http404('No access')

        if request.method == 'POST':

            # ?????????????????????? ???????????? ?? ??????????????
            project.services.add(service)

            # ?????????????????? ??????????????????
            values = request.POST.getlist("setting_value")

            for i, sid in enumerate(request.POST.getlist("setting_id")):
                try:
                    ps = ProjectServiceSetting.objects.get(
                        project_id=project.id,
                        service_id=service.id,
                        setting_id=sid,
                    )
                    ps.value = values[i]
                    ps.save()
                except ProjectServiceSetting.DoesNotExist:
                    ps = ProjectServiceSetting()
                    ps.project_id = project.id
                    ps.service_id = service.id
                    ps.setting_id = sid
                    ps.value = values[i]
                    ps.save()

            messages.success(request, '???????????? ' + service.name + ' ?????????????? ??????????????????')

            return redirect('project_detail', pk=project.id)
        else:
            ProjectServiceSettings = ProjectServiceSetting.objects.filter(
                project_id=project.id,
                service_id=service.id,
            )

            settings = {}

            for setting in ProjectServiceSettings:
                settings[setting.setting_id] = setting.value

            # for key, setting in enumerate(service.settings.all()):
            #     pass
                # service.settings[key].value = settings[setting.id]
                # print(service.settings[key])


        return render(request, 'project/service/pre_settings.html', {
            'projects': getmyprojects(request),
            'project': project,
            'service': service,
            'settings':settings,
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

    project_users = [];

    for user in project.users.values('id'):
        project_users.append(user['id'])

    if project.author_id != request.user.id and request.user.id not in project_users:
        raise Http404('No access')

    try:
        service = Service.objects.get(pk=service_id)
    except Project.DoesNotExist:
        raise Http404('No access')

    if request.method == 'POST':

        form = RunServiceForm(request.POST, request.FILES)

        if form.is_valid():

            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save('datafiles/' + myfile.name, myfile)

            J = Job()
            J.status = 1
            J.project_id = project.id
            J.service_id = service.id
            J.data = fs.url(filename)
            J.save()

            # ???????????????? ?????????????? ???????? ???? ???????????? ??????????????


            messages.success(request, '???????????? ' + service.name + ' ?????????????? ??????????????.')

            return redirect('project_service_journal', pk=project.id, service_id=service.id)
    else:
        form = RunServiceForm()


    return render(request, 'project/service/run.html', {
        'projects': getmyprojects(request),
        'project': project,
        'service': service,
        'form': form,
    })


def journal_service(request, pk, service_id, job_id=None):

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

    if (job_id is None):
        jobs = Job.objects.filter(
            project_id=project.id,
            service_id=service.id,
        ).order_by('-id')

        tpl = 'project/service/journal.html'
        results = None
    else:
        jobs = None
        tpl = 'project/service/journal_results.html'
        results = JobResult.objects.filter(job__id=job_id).order_by('-id')
        pass

    return render(request, tpl, {
        'projects': getmyprojects(request),
        'project': project,
        'service': service,
        'jobs': jobs,
        'results': results,
    })


def service_settings(request, pk, service_id):
    pass


def jobinfo(request, job_id):

    try:
        job = Job.objects.get(
            pk=job_id,
        )
    except Job.DoesNotExist:
        raise Http404('No access')

    if job.project.secret_key and job.project.secret_key != request.headers.get('authorization'):
        raise Http404('No access: ???????? ?????????????????????? ???? ????????????')

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


def jobresult(request, job_id):
    pass


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