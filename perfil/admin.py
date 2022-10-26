from django.contrib import admin
from .models import Perfil, Address

# Register your models here.

admin.site.register([Perfil, Address])