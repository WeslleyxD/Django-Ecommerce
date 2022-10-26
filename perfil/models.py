from django.db import models
from accounts.models import User

# Create your models here.

class Address(models.Model):
    state = models.CharField('Estado', max_length=30, null=True, blank=True)
    country = models.CharField('Município', max_length=30, null=True, blank=True)
    cep = models.CharField('CEP', max_length=40, null=True, blank=True)
    address = models.CharField('Endereço', max_length=254, null=True, blank=True)
    number = models.IntegerField('Número', null=True, blank=True)
    complement = models.CharField('Complemento', max_length=254, null=True, blank=True)

    class Meta:
        verbose_name = ('Address')
        verbose_name_plural = ('Address')

    def __str__(self):
        if self.address:
            return f"{self.address}"
        else:
            return f"{self.id}"


class Perfil(models.Model):

    GENDERCHOICE = [
        (1, ('Feminino')),
        (2, ('Masculino')),
        (3, ('Não responder')),
    ]

    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name=('Usuário'))
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name=('Endereço'))
    surname = models.CharField('Apelido', max_length=100, null=True, blank=True)
    cell = models.CharField('Celular', max_length=30, null=True, blank=True)
    cpf = models.CharField('Número do Documento', max_length=30, null=True, blank=True)
    birth = models.DateField('Data de Nascimento', null=True, blank=True)
    genre = models.IntegerField('Gênero', choices=GENDERCHOICE, default=3)
    #foto = models.ImageField(('Foto do Perfil'), null=True, blank=True, upload_to=profile_directory_path)
    notify_email = models.BooleanField('Notificação por Email', default=True)

    class Meta:
        verbose_name = ('Perfil')
        verbose_name_plural = ('Perfis')

    def __str__(self):
        return f"{self.user.get_full_name()} [{self.user.email}]"