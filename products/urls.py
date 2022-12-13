from django.urls import path
from .import views

app_name = 'products'

#: TODO CORRIGIR URL BUGADA
urlpatterns = [
    path('<str:category_name>/', views.product_list, name='product_list_by_category'),
    path('<str:category_name>/<slug:slug>/', views.product_detail, name='product_detail'),
]