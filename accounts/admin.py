from django.contrib import admin
from .models import User, LoginCodeVerification

# Register your models here.

admin.site.register([User, LoginCodeVerification])
