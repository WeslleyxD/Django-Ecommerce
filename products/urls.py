from django.urls import path
from .import views

app_name = 'products'

urlpatterns = [
    path('<str:category_name>/', views.product_list, name='product_list_by_category'),
    path('<str:category_name>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<str:product_id>/<str:status_likes>/<str:model>', views.like_deslike_product, name='like_deslike_product'),
    path('<str:category_name>/<slug:slug>/<str:image>/', views.product_detail, name='product_detail_image'),
]   