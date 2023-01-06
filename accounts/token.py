from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . models import User, LoginCodeVerification
from . utils import send_verification_email
from random import randrange

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
    send = send_verification_email(mail_subject, message, to_email)
    return send

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
    send = send_verification_email(mail_subject, message, to_email)
    return send

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





################################# TOKEN 2FA ##############################

def login_code_authentication(user, create=None, delete=None):
    if user and create:
        user_code = LoginCodeVerification.objects.filter(user_id=user.pk)
        if user_code:
            user_code.delete()
        token_2fa = str(randrange(111111, 999999))
        while LoginCodeVerification.objects.filter(code=token_2fa).exists():
            token_2fa = str(randrange(111111, 999999))

        code = LoginCodeVerification.objects.create(user_id=user.pk, code=token_2fa)

        #send mail
        mail_subject = 'Token de acesso'
        message = f'Olá, seu token de segurança é {code}.'
        to_email = user.email
        send_verification_email(mail_subject, message, to_email)

        return token_2fa

    if user and delete:
        LoginCodeVerification.objects.get(user_id=user.pk).delete()

        return True


############################ E-MAIL #############################

