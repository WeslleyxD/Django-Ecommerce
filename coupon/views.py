from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from cart.cart import Cart

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

@require_POST
def coupon_remove(request):

    cart = Cart(request)
    cart.remove_coupon()

    return redirect('cart:cart_detail')