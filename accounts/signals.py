import uuid
import random
import string
from .models import User
from perfil.models import Perfil, Address
from coupon.models import Coupon
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from datetime import datetime, timedelta
from django.dispatch import receiver


    # ---

@receiver(pre_save, sender=User)
def generater_username(sender, instance,**kwargs):
    if not instance.username:
        # Busca um hash aleatório para preeencher o nome do usuário
        username = uuid.uuid4().hex[:20]

        # Loop que verifica se o nome do usuário já existe
        while User.objects.filter(username=username).exists():
            # Troca o nome do usuário com outra hash
            username = uuid.uuid4().hex[:20]

        # Retorna a hash no nome do usuário
        instance.username = username

@receiver(post_save, sender=User)
def create_perfil_and_coupon(sender, instance, created, **kwargs):
    # Verifica se está criando um usuário
    if created:

        # Cria um Perfil pro User
        perfil_instance = Perfil.objects.create(
            user_id=instance.id,
        )

        # Cria um Address associado ao Perfil do User    
        Address.objects.create(perfil=perfil_instance)

        # Cria um Coupon associado ao Perfil do User
        coupon_code = ''.join(random.choices(population=string.ascii_uppercase+string.digits, k=8))

        Coupon.objects.create(
            perfil=perfil_instance,
            code=coupon_code,
            valid_to=datetime.now() + timedelta(days=30),
            discount=20
        )


# @receiver(post_save, sender=Perfil)
# def create_address(sender, instance, created, **kwargs):
#     print(instance)
#     print(dir(instance))
#     # Verifica se está criando um usuário
#     if created:
#         Address.objects.create(id=instance.id)
#         # ---
#     # ---