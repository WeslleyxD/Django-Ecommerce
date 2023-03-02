from .models import User, LoginCodeVerification
from .forms import UserCreateForm, LoginForm, EmailToPasswordResetForm, ResetPasswordForm, LoginCodeVerificationForm
from .token import check_token_verified_email, generate_token_verified_email, password_reset_token, check_token_password_reset, generate_token_password_reset, login_code_authentication
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def login_user(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None and user.twofa:
                token_2fa = login_code_authentication(user, create=True)
                # PAREI AQUI, PEGA O TOKEN PARA ENVIAR O EMAIL
                #print (token_2fa)
                #login(request, user)
                #return redirect('perfil:my_perfil')
                return redirect('accounts:login_twofa_authentication')
            elif user is not None:
                request.session['user_pk'] = user.pk
                # request.session['fav_color'] = 'blue'
                # request.session['products'] = {'celular': '1'}
                # print (dir(request.session))
                # print ('*' * 50)
                login(request, user)
                if 'next' in request.META['HTTP_REFERER']:
                    return redirect(request.META['HTTP_REFERER'].split('next=')[1])

                return redirect ('perfil:my_perfil')

    return render(request, 'accounts/login.html', {'login_form': login_form})

def login_twofa_authentication(request, resend_mail=None):
    if resend_mail:
        user_pk = request.session.get('user_pk')
        user = get_object_or_404(User, pk=user_pk)
        login_code_authentication(user, create=True)
        return redirect('accounts:login_twofa_authentication')
    login_code_form = LoginCodeVerificationForm()
    if request.method == 'POST':
        login_code_form = LoginCodeVerificationForm(request.POST)
        if login_code_form.is_valid():
            user_pk = request.session.get('user_pk')
            user = get_object_or_404(User, pk=user_pk)
            cd = login_code_form.cleaned_data
            try:
                if user.logincodeverification.code == cd['code']:
                    login(request, user, backend='accounts.backends.EmailBackend')
                    login_code_authentication(user, delete=True)
                    return redirect('core:index')
                else:
                    login_code_form.add_error(None, "Código de segurança inválido.")
                    return render(request, 'accounts/login_2fa.html', {'login_code_form': login_code_form})
            except Exception:
                #.add_error(None, 'TEXT') adiciona erro no def non_field_errors do form
                login_code_form.add_error(None, "Código de segurança inválido")
                return render(request, 'accounts/login_2fa.html', {'login_code_form': login_code_form})

    return render(request, 'accounts/login_2fa.html', {'login_code_form': login_code_form})

def logout_user(request):    

    #Remove as sessões expiradas da tabela Session
    # request.session.clear_expired()

    logout(request)
    return redirect('accounts:login_user')

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
            return render(request, 'accounts/password_reset_done.html')
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
