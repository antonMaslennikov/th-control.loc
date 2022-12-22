from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Count, Q
from project.models import Project, Invite, UsersRelation, Service
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from .forms import ProjectForm, InviteForm
import random, string
from django.contrib import messages


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
    if (password):
        UsersRelation(user=user, project=invite.project).save()

    login(request, user)

    # помечаем инвайт как использованный
    invite.accepted = True
    invite.accepted_at = timezone.datetime.now()
    invite.save()

    # set flash message
    messages.success(request, 'Инвайт был успешно принят.' + (' Данные для входа отправлены на Ваш email ' + invite.email if password else ''))

    return redirect('project_detail', pk=invite.project.id)


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

    services = Service.objects.all()

    if (service_id is None):
        template = 'project/service/connect.html'
    else:
        template = 'project/service/pre_settings.html'



    return render(request, template, {
        'projects': getmyprojects(request),
        'project': project,
        'services': services,
        # 'form': form,
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