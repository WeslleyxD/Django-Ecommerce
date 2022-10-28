from django.shortcuts import render
from django.shortcuts import get_object_or_404
from products.models import Category, Product
from products.forms import SearchForm
from django.db import connection, reset_queries

# Create your views here.

def index(request, category_name=None):
    search_form = SearchForm()
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_name:
        products = products.filter(category=category)

    return render(request, 'index.html',
                {'category': category,
                'categories': categories,
                'products': products,
                'search_form': search_form}
    )