from accounts.models import User
from .models import Address, Perfil
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete


@receiver(post_save, sender=User)
def create_perfil(sender, instance, created, **kwargs):
    # Verifica se está criando um usuário
    if created:
        # Cria um Address e associa ao Perfil criado
        address_id = Address.objects.create()
        Perfil.objects.create(user_id=instance.id, address_id=address_id.id)
    # ---
