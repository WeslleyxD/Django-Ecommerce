from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.conf import settings
from django.views.decorators.cache import cache_page
from os import environ

def product_list(request, category_name):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)

    return render(request,
                'index.html',
                {'category': category,
                'categories': categories,
                'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request,
    'products/list.html',
    {'product': product})