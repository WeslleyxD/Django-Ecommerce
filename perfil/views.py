import json
from django.shortcuts import render, redirect
from . forms import AddressForm, PerfilForm
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
        form = AddressForm(instance=request.user.perfil.address)
    if fk == 'perfil':
        form = PerfilForm(instance=request.user.perfil)

    if request.method == 'POST':
        if fk == 'user':
            form = UserCreateForm(request.POST, instance=request.user)
        if fk == 'address':
            form = AddressForm(request.POST, instance=request.user.perfil.address)
            #return render(request, 'perfil/my_perfil_foreignkey.html', {'form':form, 'relation':fk})
                
        if fk == 'perfil':
            form = PerfilForm(request.POST, instance=request.user.perfil)

        print (form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            form.save()
            return redirect('perfil:my_perfil_foreignkey', fk=fk)

    return render(request, 'perfil/my_perfil.html', {'form':form, 'relation':fk})