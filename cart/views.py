from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateProductForm
from coupon.forms import CouponApplyForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print (cd)
        cart.add(product=product, quantity=cd['quantity'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.update(product=product, quantity=cd['quantity'])
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['add_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity']})
        item['update_quantity_form'] = CartUpdateProductForm(initial={'quantity': item['quantity']})

    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})