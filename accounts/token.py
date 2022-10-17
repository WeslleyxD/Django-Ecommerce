from django.contrib.auth.tokens import PasswordResetTokenGenerator
from http.client import HTTPResponse
from re import template
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def generate_token_verified_email(request, user, to_email):
    mail_subject = 'active your e-mail'
    message = render_to_string(template_name='accounts/register_email_confirm.html', 
    context= {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    send = send_verification_email(mail_subject, message, settings.EMAIL_FROM, to_email)
    return send
    
def send_verification_email(mail_subject, message, from_email, to_email):
    try:
        email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
        if email.send():
            return True
    except Exception as e:
        print (e)
        return False

def check_token_verified_email(uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and email_activation_token.check_token(user, token):
        user.verification_email=True
        user.save()
        return True
    else:
        False


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ((user.pk) + (timestamp) + (user.verification_email))

email_activation_token = AccountActivationTokenGenerator()


########################-#########################################-###########################


def generate_token_password_reset(request, user, to_email):
    mail_subject = 'Altere sua senha'
    message = render_to_string(template_name='accounts/password_reset_confirm.html', 
    context= {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    send = send_verification_email(mail_subject, message, settings.EMAIL_FROM, to_email)
    return send
    
def send_verification_email(mail_subject, message, from_email, to_email):
    try:
        email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
        if email.send():
            return True
    except Exception as e:
        print (e)
        return False

def check_token_password_reset(uidb64, token, password):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        if user.password_change == False:
            user.password_change = True
        else:
            user.password_change = False
        user.set_password(str(password))
        user.save()
        return True
    else:
        False

class PasswordResettTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ((user.pk) + (timestamp) + (user.password_change))
        
password_reset_token = PasswordResettTokenGenerator()