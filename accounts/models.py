from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='Usuário',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ("Esse usuário já existe, favor selecionar outro."),
        },
    )
    first_name = models.CharField(verbose_name='Nome', max_length=254)
    last_name = models.CharField(verbose_name='Sobrenome', max_length=254)
    email = models.EmailField(
        verbose_name='E-mail',
        unique=True,         
        error_messages={
            'unique': ("Esse e-mail já existe, favor selecionar outro."),
        }
    )
    is_staff = models.BooleanField(verbose_name='É membro', default=False)
    is_active = models.BooleanField(verbose_name='É ativo', default=True)
    password_change = models.BooleanField(default=False)
    #verified = models.BooleanField(default=False, editable=False)
    verification_email = models.BooleanField(verbose_name='E-mail verificado', default=False)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modificado em', auto_now=True)
    deleted = models.BooleanField(verbose_name='Deletado', default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    class Meta:
        verbose_name = ('Usuário')
        verbose_name_plural = ('Usuários')
        ordering = ['first_name', 'last_name', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self):
        self.deleted = True
        self.save()
    
