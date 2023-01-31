from django.contrib import admin
from .models import Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['address']
    prepopulated_fields = {'slug': ('address',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['perfil']
    list_filter = ['finish', 'created', 'updated']

    inlines = [OrderItemInline]



admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)