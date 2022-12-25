from distutils.command.clean import clean
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Product

class SearchForm(forms.Form):
    search = forms.CharField(max_length=300)

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }