from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic

from .forms import UserRegistrationForm
from .tokens import account_activation_token


def singup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # дублируем в поле логина email
            new_user.username = new_user.email
            # по умолчанию не активируем
            new_user.is_active = False
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password1'])
            # Save the User object
            new_user.save()

            # to get the domain of the current site 
            current_site = get_current_site(request) 
            mail_subject = 'Activation link has been sent to your email id' 
            message = render_to_string('registration/acc_active_email.html', { 
                'user': new_user, 
                'domain': current_site.domain, 
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)), 
                'token':account_activation_token.make_token(new_user), 
            }) 
            to_email = form.cleaned_data.get('email') 
            email = EmailMessage( 
                mail_subject, message, to=[to_email] 
            )
            email.send() 

            return render(request, 'accounts/signup_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})



def activate(request, uidb64, token): 
    User = get_user_model()
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 

    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.') 
        return render(request, 'accounts/activate.html', {'result': 'success'})
    else: 
        # return HttpResponse('Activation link is invalid!')
        return render(request, 'accounts/activate.html', {'result': 'error'})