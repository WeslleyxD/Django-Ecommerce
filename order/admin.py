from django.contrib import admin
from .models import Order

admin.site.register([Order])

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['address']
    prepopulated_fields = {'slug': ('address',)}