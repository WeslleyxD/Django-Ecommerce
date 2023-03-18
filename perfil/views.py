import json
from django.shortcuts import render, redirect
from . forms import AddressForm, PerfilForm
from order.models import Order
from coupon.forms import CouponForm
from accounts.forms import UserCreateForm
from . utils import via_cep
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def my_perfil(request, fk=None):
    form = None
    if fk == 'user':
        form = UserCreateForm(instance=request.user)
    if fk == 'address':
        form = AddressForm(instance=request.user.perfil.address.get(selected=True))
    if fk == 'perfil':
        form = PerfilForm(instance=request.user.perfil)
    if fk == 'coupons':

        ok = request.user.perfil.coupons.all()[0]
        print (ok)
        form = CouponForm(instance=ok)

    # if fk == 'Order':
    #     form = 

    if request.method == 'POST':
        if fk == 'user':
            form = UserCreateForm(request.POST, instance=request.user)
        if fk == 'address':
            form = AddressForm(request.POST, instance=request.user.perfil.address.get(selected=True))
            #return render(request, 'perfil/my_perfil_foreignkey.html', {'form':form, 'relation':fk})
        if fk == 'perfil':
            form = PerfilForm(request.POST, instance=request.user.perfil)
        if fk == 'coupons':
            form = CouponForm(request.POST, instance=request.user.perfil.all()[0].id)

        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect('perfil:my_perfil_foreignkey', fk=fk)

    return render(request, 'perfil/my_perfil.html', {'form':form, 'relation':fk})