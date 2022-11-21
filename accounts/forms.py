from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):

    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='Имя', max_length=100, required=False)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже зарегистрирован у нас в системе.")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']