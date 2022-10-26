from distutils.command.clean import clean
from django.contrib.auth import authenticate, password_validation
from accounts.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from captcha.fields import ReCaptchaField, ReCaptchaV2Checkbox
from captcha.widgets import ReCaptchaV2Invisible

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', 
        widget=forms.PasswordInput(attrs={"class": "login-form-attr"}),
    )
    password2 = forms.CharField(label='Confirme a senha', 
        widget=forms.PasswordInput(attrs={"class": "login-form-attr"}),
    )
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox(attrs={}))
    
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password1', 'password2', 'captcha')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "login-form-attr"}),
            'last_name': forms.TextInput(attrs={"class": "login-form-attr"}),
            'email': forms.EmailInput(attrs={"class": "login-form-attr"}),
            }

    # def clean_username(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     if 'ok' in username:
    #         raise ValidationError(
    #             "username testando xd"
    #         )
    #     return username

    #TODO: VALIDAR FORM REGISTER
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'), max_length=200, required=True,
    widget=forms.TextInput(attrs={"class": "login-form-attr"})
    )
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class":"login-form-attr"}),
    )

    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox(attrs={}))
    error_messages = {
        "invalid_login": _(
            "E-mail ou senha incorreto."
        ),
        "invalid_password": _ (
            "Faltou verificar o recaptcha."
        )
        #"inactive": _("This account is inactive."),
    }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     password = cleaned_data.get("password")
    #     if User.objects.filter(username__iexact=username):
    #         ok = User.objects.get(username__iexact=username)
    #         print (dir(ok))
    #         print (ok.set_password)
    #         msg = "Usuário ou senha incorreto"
    #         self.add_error('username', msg)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("email")
        password = cleaned_data.get("password")
        captcha = cleaned_data.get('captcha')
        if not authenticate(username=username, password=password):
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="inactive",
            )
        if not captcha:
            raise ValidationError(
            self.error_messages["invalid_password"],
            code="inactive",
            )
        return cleaned_data


class EmailToPasswordResetForm(forms.Form):
    email = forms.EmailField(
    label=_("Email"),
    max_length=254,
    widget=forms.EmailInput(attrs={"autocomplete": "email"}),
)
    error_messages = {
        "invalid_email": _(
            "E-mail inserido inválido, tente novamente."
        ),
    }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not User.objects.filter(email__iexact=email):
            raise ValidationError(
                self.error_messages["invalid_email"],
                code="inactive",
            )
        return cleaned_data

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
        strip=False,
    )
    error_messages = {
        "invalid_password": _(
            "Senhas não são guais"
        ),
        "senha_pequena": _(
            "Senha menor que 8 caracteres"
        ),
    }
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(
                self.error_messages["invalid_password"],
                code="inactive",
            )
        if len(password1) < 8:
            raise ValidationError(
                self.error_messages["senha_pequena"],
                code="inactive",
            )
        
        return cleaned_data