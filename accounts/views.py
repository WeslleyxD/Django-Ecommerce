from cgitb import reset
from pdb import post_mortem
from django.shortcuts import render
from .forms import UserCreateForm, LoginForm, EmailToPasswordResetForm, ResetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from http.client import HTTPResponse
from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from  django.contrib.auth import get_user_model
from .token import email_activation_token, check_token_verified_email, generate_token_verified_email, password_reset_token, check_token_password_reset, generate_token_password_reset
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from .decorators import user_is_entry_author
# Create your views here.
def login_user(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('core:index')
            return render(request, 'accounts/login.html', {'login_form': login_form})
    return render(request, 'accounts/login.html', {'login_form': login_form})

def logout_user(request):
    logout(request)
    return redirect('accounts:login_user')

'TODO:em breve'
def profile_user(request):
    user_form = UserCreateForm(instance=request.user)
    if request.method == 'POST':
        
        if user_form.is_valid():
            print ('ok')
    return render(request, 'accounts/profile_user.html', {'user_form': user_form})

def verification_email(request):
    if 'accounts/profile/' in request.META.get('HTTP_REFERER', {}):
        user = request.user
        to_email = user.email
        if not request.user.verification_email:
            generate_token_verified_email(request, user, to_email)
        return render(request, 'accounts/verification_email.html')
    else:
        return render(request, 'error404.html')

def register(request):
    user_form = UserCreateForm()
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = user_form.save()
            generate_token_verified_email(request, user, cd['email'])
            return render(request, 'accounts/register_sucess.html')
        else:
            user_form = UserCreateForm(request.POST)
    return render(request, 'accounts/register.html', {'user_form': user_form})

def register_email_confirm(request, uidb64, token):
    check_token = check_token_verified_email(uidb64, token)
    if check_token:
        return render(request, 'accounts/register_email_confirm_sucess.html')
    else:
        return render(request, 'accounts/register_email_confirm_error.html')


#FORGET PASSWORD
def password_reset(request):
    password_reset_form = EmailToPasswordResetForm()
    if request.method == 'POST':
        password_reset_form = EmailToPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            to_email = password_reset_form.cleaned_data
            user = User.objects.get(email=to_email['email'])
            generate_token_password_reset(request, user, to_email['email'])
    return render(request, 'accounts/password_reset.html', {'password_reset_form': password_reset_form})

def password_reset_confirm(request, uidb64, token):
    reset_password_form = ResetPasswordForm()
    
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    check_token = password_reset_token.check_token(user, token)

    if check_token:
        if request.method == 'POST':
            reset_password_form = ResetPasswordForm(request.POST)
            if reset_password_form.is_valid():
                cd = reset_password_form.cleaned_data
                check_token = check_token_password_reset(uidb64, token, cd['password1'])
                if check_token:
                    #user = User.objects.filter(username=check_token)
                    return render(request, 'accounts/password_reset_confirm_sucess.html')
                else:
                    return render(request, 'accounts/password_reset_confirm_error.html')
        return render(request, 'accounts/password_reset_form.html',{'reset_password_form': reset_password_form, 'uidb64': uidb64, 'token': token})  
    else:
        return render(request, 'accounts/password_reset_confirm_error.html')
