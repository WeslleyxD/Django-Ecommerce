from django.shortcuts import render
from django.shortcuts import get_object_or_404
from products.models import Category, Product
from products.forms import SearchForm
from django.db import connection, reset_queries
from django.core.signing import Signer
from products.utils import pagination
from django.core.mail import send_mail

# Create your views here.

def index(request, category_name=None):
    search_form = SearchForm()
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_name:
        products = products.filter(category=category)

    page_obj = pagination(request, products, 4)

    
    ok = render(request, 
                'index.html',
                {'category': category,
                'categories': categories,
                'search_form': search_form,
                'page_obj': page_obj}
        )



    #ok['Set-Cookie'] = 'commida=jujuba'
    # ok['Content-Type'] = 'application/json'
    # # ok['Content'] = {'weslley': '123'}
    # xd = ok
    # signer = Signer()

    # xd.set_signed_cookie('test', signer.sign_object({'message': 'Hello!'}),
#)

    #dir(xd))
    #xd.cookies['test'])
    # test = (request.get_signed_cookie('test'))
    # test)
    # printa =  signer.unsign_object(test)
    # printa)
    return ok


def testando(request):
    return render(request, 
                'testando.html',
        )
