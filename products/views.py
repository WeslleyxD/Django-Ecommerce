from .models import Category, Product, Image, User, Comment
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from products.utils import pagination
from .forms import ProductModelForm, CommentModelForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
#from django.db import connection, reset_queries

def product_list(request, category_name=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_name:
        category = get_object_or_404(Category, name=category_name.lower())
        products = Product.objects.filter(category=category).filter(available=True).select_related('category').select_related('brand')
    
    page_obj = pagination(request, products, 3)

    return render(request, 
                'products/list.html',
                {'category': category,
                'page_obj': page_obj,
            })

def product_detail(request, category_name, slug, image=None):
    #Produto selecionado no template list products
    product = get_object_or_404(Product, slug__iexact=slug, available=True)

    #Primeira imagem a aparecer do produto
    image_first = product.image.first()

    #Alguma imagem selecionada
    image_selected = None
    if image:
        image_selected = product.image.get(id=image)

    #Pagination images
    page_images = pagination(request, product.image.all().order_by('id'), 4)

    #Commentários
    comment_form = CommentModelForm()


    #print(dir(ok))
    #print (dir(ok.product))

    return render(request, 
                'products/detail_item.html', 
                {
                    'product': product,
                    'image_selected': image_selected,
                    'image_first': image_first,
                    'page_images': page_images,
                    'comment_form': comment_form,
                }
            )

@login_required()
@require_POST
def like_deslike_product(request, product_id=None, status_likes=None):
    product = get_object_or_404(Product, id=product_id)

    #product.like.remove(request.user)

    if status_likes == 'like':
        product.like.remove(request.user.id) if product.like.filter(id=request.user.id).exists() else product.like.add(request.user)

    if status_likes == 'deslike':
        product.deslike.remove(request.user.id) if product.deslike.filter(id=request.user.id).exists() else product.deslike.add(request.user)


    return redirect (request.META['HTTP_REFERER'])

    #{'product': product})