from .models import User
from django.shortcuts import redirect, render



#TESTANDO DECORATORS
def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        if 'accounts/profile/' not in request.META.get('HTTP_REFERER', {}):
            print (1)
        else:
            print (1)
    return wrap