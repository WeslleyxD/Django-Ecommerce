from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateProductForm
from coupon.forms import CouponApplyForm
from coupon.models import Coupon

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
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
    coupon_apply_form = CouponApplyForm()

    cart = Cart(request)
    for item in cart:
        item['add_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity']})
        item['update_quantity_form'] = CartUpdateProductForm(initial={'quantity': item['quantity']})

    if request.method == 'POST':
        coupon_apply_form = CouponApplyForm(request.POST, perfil_id=(request.user.perfil.id if request.user.is_authenticated else None))
        
        if coupon_apply_form.is_valid():
            cart = Cart(request)
            cart.clean_to_post()

            code = coupon_apply_form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, active=True)
                if coupon.valited_coupon():
                    request.session['coupon_id'] = coupon.id
                else:
                    request.session['coupon_id'] = None  
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None

            return redirect('cart:cart_detail')
        return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})

    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})