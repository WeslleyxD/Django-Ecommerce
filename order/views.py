from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from perfil.models import Perfil
from accounts.models import User
from coupon.models import Coupon
from django.db import connection, reset_queries
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        #request.POST.update({'TESTE': ['123']})

        # print (dir(request.user))
        # print (1000000)
        # print (dir(request.user.perfil))
        # print (dir(request.user.perfil.address_set.get(selected=True)))
        
        user = request.user
        perfil = request.user.perfil
        address = request.user.perfil.address.get(selected=True)
        #print (cd)

        order = Order.objects.create(
            perfil=perfil,
            address=address.get_full_address(),
            email=user.email,
            cep=address.cep,
        )

        if cart.coupon_id is not None:
            # Desativando o Coupon
            coupon = cart.coupon
            coupon.active = False
            coupon.used_at = timezone.now()
            coupon.save()

            # Inserindo o Coupon na Order
            order.coupon = cart.coupon
            order.save()

        print (len(connection.queries))
        reset_queries()
        for item in cart:
            OrderItem.objects.create(order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity'])
        cart.clean()
        cart.clean_coupon()
        return render(request,
                    'order/created.html',
                    {})

    return render(request,
                'order/create.html',
                {'cart': cart,})
