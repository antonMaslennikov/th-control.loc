from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserRegistrationForm
 
def singup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # дублируем в поле логина email
            new_user.username = new_user.email
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            return render(request, 'accounts/signup_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})