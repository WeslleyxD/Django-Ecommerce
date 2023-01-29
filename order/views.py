from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    print (1)
    if request.method == 'POST':
        print (2)
        form_order = OrderCreateForm(request.POST)
        if form_order.is_valid():
            cd = form_order.cleaned_data
            print (cd)
            order = form_order.save(commit=False)
            order.user = request.user.perfil
            order.save()
            print (order)
            for item in cart:
                OrderItem.objects.create(order=order,
                                product=item['product'],
                                price=item['price'],
                                quantity=item['quantity'])
            cart.clear()
            return render(request,
                        'order/created.html',
                        {'form_order': form_order})

    return render(request,
                'order/create.html',
                {'cart': cart, 'form_order': form_order})
