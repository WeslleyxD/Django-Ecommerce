from .models import Category, Product, Image, User, Comment
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from products.utils import pagination
from .forms import ProductModelForm, CommentModelForm
from cart.forms import CartAddProductForm
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
    cart_product_form = CartAddProductForm()
    #Commentários
    comment_form = CommentModelForm()
    #Desabilita o botão de submit se o usuário logado já comentou no product
    button_status = None
    #Desabilita o comentário se o user já comentou neste produto.
    # if product.comment.filter(user=request.user).exists():
    #     button_status = True
    #     for field in comment_form:
    #         field.field.widget.attrs.update({"class": "comment-form-attr-block", "readonly": True, "placeholder": "Você já comentou este produto"})

    #Primeira imagem a aparecer do produto
    image_first = product.image.first()

    #Alguma imagem selecionada
    image_selected = None
    if image:
        image_selected = product.image.get(id=image)

    #Pagination images
    page_images = pagination(request, product.image.all().order_by('id'), 4)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            print (request.path)
            return redirect(f'/accounts/login/?next={request.path}')
            #return render(request, 'accounts/login.html')
        # if product.comment.filter(user=request.user).exists():
        #     comment_form = CommentModelForm()
        #     button_status = True
        #     for field in comment_form:
        #         field.field.widget.attrs.update({"class": "comment-form-attr-block", "readonly": True, "placeholder": "Você já comentou este produto" })
        else:
            comment_form = CommentModelForm(data=request.POST)
            if comment_form.is_valid():
                save_comment_form = comment_form.save(commit=False)

                #Salvando as informações essenciais pro comentário aparecer
                save_comment_form.user = request.user
                save_comment_form.product = product
                save_comment_form.save()

                comment_form = CommentModelForm()
                button_status = True
                for field in comment_form:
                    field.field.widget.attrs.update({"class": "comment-form-attr-block", "readonly": True, "placeholder": "Você já comentou este produto" })


    return render(request, 
                'products/detail_item.html', 
                {
                    'product': product,
                    'image_selected': image_selected,
                    'image_first': image_first,
                    'page_images': page_images,
                    'comment_form': comment_form,
                    'button_status': button_status,
                    'cart_product_form': cart_product_form
                }
            )

@login_required()
@require_POST
def like_deslike_product(request, product_id=None, status_likes=None, model=None):
    #product.like.remove(request.user)
    if model.lower() == 'product':
        product = get_object_or_404(Product, id=product_id)
        if status_likes == 'like':
            product.like.remove(request.user.id) if product.like.filter(id=request.user.id).exists() else product.like.add(request.user)

        if status_likes == 'deslike':
            product.deslike.remove(request.user.id) if product.deslike.filter(id=request.user.id).exists() else product.deslike.add(request.user)

        return redirect (request.META['HTTP_REFERER'])

    if model.lower() == 'comment':
        comment = get_object_or_404(Comment, id=product_id)
        if status_likes == 'like':
            comment.like.remove(request.user.id) if comment.like.filter(id=request.user.id).exists() else comment.like.add(request.user)

        if status_likes == 'deslike':
            comment.deslike.remove(request.user.id) if comment.deslike.filter(id=request.user.id).exists() else comment.deslike.add(request.user)

        return redirect (request.META['HTTP_REFERER'])
