from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.my_perfil, name='my_perfil'),
    path('<str:fk>', views.my_perfil, name='my_perfil_foreignkey'),
]