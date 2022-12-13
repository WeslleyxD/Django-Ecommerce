from .models import Category, Product
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from products.utils import pagination
#from django.db import connection, reset_queries

def product_list(request, category_name=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = Product.objects.filter(category=category).filter(available=True).select_related('category').select_related('brand')
    page_obj = pagination(request, products, 3)

    return render(request, 
                'products/list.html',
                {'category': category,
                'page_obj': page_obj
            })

def product_detail(request, category_name, slug):
    product = get_object_or_404(Product, slug__iexact=slug, available=True)
    print (product)
    #print (product)
    return render(request, 'products/detail_item.html')
    #{'product': product})  