from .models import User
from django.shortcuts import redirect, render

def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        if 'accounts/profile/' not in request.META.get('HTTP_REFERER', {}):
            pass
        else:
            pass
    return wrap

