from distutils.command.clean import clean
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserCreateForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Usuário', 'title': 'Your name','size': "40"}), 
            'email': forms.EmailInput(attrs={'placeholder':'E-mail',}),
            }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    # def clean_username(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     if 'ok' in username:
    #         raise ValidationError(
    #             "username testando xd"
    #         )

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Usuário'), max_length=200, required=True)
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Usuário ou senha incorreto."
        ),
        "invalid_password": _ (
            "Senha errada, tente novamente."
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
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not authenticate(username=username, password=password):
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="inactive",
            )
        return cleaned_data

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if username == 'test':
    #         raise ValidationError(
    #             self.error_messages["invalid_login"],
    #             code="inactive",
    #             params={'username':20}
    #         )
    #     else:
    #         return username

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