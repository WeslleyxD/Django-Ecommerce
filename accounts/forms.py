from .models import User, LoginCodeVerification
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField, ReCaptchaV2Checkbox

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(),)
    
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "password_small": _("A senha deve conter pelo menos 8 caracteres."),
        "email_exists": "E-mail fornecido já existe",
    }

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password1', 'password2', ) #'captcha')
        widgets = {
            # 'first_name': forms.TextInput(attrs={"class": "login-form-attr"}),
            # 'last_name': forms.TextInput(attrs={"class": "login-form-attr"}),
            # 'email': forms.EmailInput(attrs={"class": "login-form-attr"}),
            # 'twofa': forms.CheckboxInput(attrs={"class": "login-form-attr"},)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            instance = self.fields[field]
            if instance.required == True:
                instance.label_suffix = " *"

            if field == 'twofa':
                print (dir(instance))
                print ((instance))
    # def clean_username(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     if 'ok' in username:
    #         raise ValidationError(
    #             "username testando xd"
    #         )
    #     return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        if len(password1) < 7 or len(password2) < 7:
            raise ValidationError(
                self.error_messages["password_small"],
                code="password_small",
            )
        if User.objects.filter(email__icontains=cleaned_data.get('email')).exists():
            raise ValidationError(
                self.error_messages["email_exists"],
                code="email_exists",
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print (self.cleaned_data['password1'])
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

    prefix = 'login'

    #captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox(attrs={}))
    error_messages = {
        "invalid_login": _(
            "E-mail ou senha incorreto"
        ),
        "invalid_password": _ (
            "Faltou verificar o recaptcha"
        )
        #"inactive": _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            instance = self.fields[field]
            if instance.required == True:
                instance.label_suffix = " *"
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("email")
        password = cleaned_data.get("password")
        # captcha = cleaned_data.get('captcha', """  """{})
        if not authenticate(username=username, password=password):
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="inactive",
            )
        # if not captcha:
        #     raise ValidationError(
        #     self.error_messages["invalid_password"],
        #     code="inactive",
        #     )
        # return cleaned_data


class EmailToPasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=254, widget=forms.EmailInput(attrs={"class": "login-form-attr"}),)
    error_messages = {
        "invalid_email": _(
            "E-mail inserido inválido, tente novamente."
        ),
    }
    prefix = 'forget'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     if not User.objects.filter(email__iexact=email).exists():
    #         raise ValidationError(
    #             self.error_messages["invalid_email"],
    #             code="inactive",
    #         )
    #     return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            instance = self.fields[field]
            if instance.required == True:
                instance.label_suffix = " *"

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label='Senha', 
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "login-form-attr"}),
    )
    password2 = forms.CharField(label='Confirme a senha', 
        widget=forms.PasswordInput(attrs={"class": "login-form-attr"}),
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


class LoginCodeVerificationForm(forms.ModelForm):
    class Meta:
        model = LoginCodeVerification
        fields = ['code']
        widgets = {
            'code': forms.TextInput(),}
        labels = {
            "code": _("Código de segurança"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"login-form-attr"})

    def clean(self):
        cleaned_data = super().clean()
        if 'a' == 8:
            raise ValidationError(
                self.error_messages["senha_pequena"],
                code="inactive",
            )
        self.add_error
        print (cleaned_data)
        return cleaned_data