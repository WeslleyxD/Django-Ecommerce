from django.db import models
from accounts.models import User
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Perfil(models.Model):

    GENDERCHOICE = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('N', 'Não responder'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=('Usuário'))
    cell = models.CharField('Celular', max_length=11, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, null=True)
    birth = models.DateField('Data de Nascimento', null=True, blank=True)
    genre = models.CharField('Gênero', max_length=1, choices=GENDERCHOICE, default='N')
    #foto = models.ImageField(('Foto do Perfil'), null=True, blank=True, upload_to=profile_directory_path)
    notify_email = models.BooleanField('Notificação por Email', default=True)

    class Meta:
        verbose_name = ('Perfil')
        verbose_name_plural = ('Perfis')

    def __str__(self):
        return f"{self.user.get_full_name()} [{self.user.email}]"

    def get_all_relations(self):
        return ['user', 'address', 'perfil']



class Address(models.Model):

    STATES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
    ('DF', 'Distrito Federal'),
    ]

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True, related_name='address', verbose_name='perfil')
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    state = models.CharField('Estado', max_length=200, null=True, blank=True, choices=STATES)
    city = models.CharField('Cidade', max_length=20, null=True, blank=True)
    district = models.CharField('Bairro', max_length=100, null=True, blank=True)
    address = models.CharField('Logradouro', max_length=254, null=True, blank=True)
    number = models.CharField('Número', max_length=10, null=True, blank=True)
    complement = models.CharField('Complemento', max_length=254, null=True, blank=True)
    selected = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Address')
        verbose_name_plural = ('Address')

    def __str__(self):
        return f"{self.address} {self.cep}"

    def get_full_address(self):
        return f"{self.state} {self.city} {self.district} {self.address} {self.number} {self.complement}"
        
    # def get_absolute_url(self):
    #     return reverse('perfil:product_list_by_category', args=[self.slug])

