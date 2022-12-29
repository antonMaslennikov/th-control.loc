import os

from django import forms
from django.core.exceptions import ValidationError

from .models import Project, Invite
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class ProjectForm(forms.ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['types'].widget.attrs.update({'class': 'form-control'})
        self.fields['regions'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_service'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['secret_key'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Project
        fields = ['name', 'url', 'types', 'regions', 'is_service', 'secret_key']


class InviteForm(forms.ModelForm):

    project = None

    def __init__(self, *args, **kwargs):

        self.project = kwargs.pop('project')

        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = Invite
        fields = ['email']

    def clean_email(self):
        data = self.cleaned_data['email']

        # проверка, что пользователь с таким мылом уже не привязан к этому проекту
        for u in self.project.users.values():
            if u['email'] in data:
                raise ValidationError("Этот пользователь уже участвует в проекте")

        # и это не сам хозяин проекта
        if self.project.author.email == data:
            raise ValidationError("Вы не можете пригласить себя в проект")

        return data

    def send_email(self, invite, request):

        current_site = get_current_site(request)
        mail_subject = 'Invite to project'
        message = render_to_string('project/invite_email.html', {
            'invite': invite,
            'domain': current_site.domain,
        })
        to_email = self.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()


class RunServiceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

    file = forms.FileField()

    def clean_file(self):
        data = self.cleaned_data['file']

        valid_extensions = ['.txt', '.xlsx']

        if not os.path.splitext(data.name)[1] in valid_extensions:
            raise ValidationError("Файл должен иметь расширение txt или xlsx")

        return data