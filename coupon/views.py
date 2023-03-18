from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from cart.forms import CartAddProductForm, CartUpdateProductForm
from cart.cart import Cart

from django.contrib.auth.decorators import login_required



@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            if coupon.valited_coupon():
                request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
    else:
        cart = Cart(request)
        for item in cart:
            item['add_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity']})
            item['update_quantity_form'] = CartUpdateProductForm(initial={'quantity': item['quantity']})
        return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': form})
        



@require_POST
def coupon_remove(request):

    cart = Cart(request)
    cart.remove_coupon()

    return redirect('cart:cart_detail')