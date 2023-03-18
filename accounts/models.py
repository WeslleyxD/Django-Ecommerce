from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin
from captcha.fields import ReCaptchaField

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Usuário',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ("Esse usuário já existe, favor selecionar outro."),
        },
    )
    first_name = models.CharField('Nome', max_length=254)
    last_name = models.CharField('Sobrenome', max_length=254)
    email = models.EmailField(
        'E-mail',
        unique=True,         
        error_messages={
            'unique': ("Esse e-mail já existe, favor selecionar outro."),
        }
    )
    is_staff = models.BooleanField('É membro', default=False)
    is_active = models.BooleanField('É ativo', default=True)
    password_change = models.BooleanField(default=False)
    #verified = models.BooleanField(default=False, editable=False)
    verification_email = models.BooleanField('E-mail verificado', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    modified_at = models.DateTimeField('Modificado em', auto_now=True)
    deleted = models.BooleanField('Deletado', default=False)
    twofa = models.BooleanField('Autenticação em duas etapas', default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email',]

    objects = UserManager()

    class Meta:
        verbose_name = ('Usuário')
        verbose_name_plural = ('Usuários')
        ordering = ['first_name', 'last_name', ]

    def __str__(self):
        return f'{self.get_full_name()} {self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self):
        self.deleted = True
        self.save()

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         print (self.password)
    #         self.set_password(self.password)
    #     super().save(*args, **kwargs)


class LoginCodeVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code_verification')
    code = models.CharField(max_length=6)

    def __str__(self):
        return str(self.code)