import uuid
from .models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete

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

# @receiver(post_save, sender=Perfil)
# def create_address(sender, instance, created, **kwargs):
#     print(instance)
#     print(dir(instance))
#     # Verifica se está criando um usuário
#     if created:
#         Address.objects.create(id=instance.id)
#         # ---
#     # ---