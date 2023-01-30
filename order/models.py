from django.db import models
from products.models import Product
from decimal import Decimal
from coupon.models import Coupon
from perfil.models import Perfil

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Perfil, related_name='perfil', on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, related_name='coupon', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300)
    email = models.EmailField()
    cep = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    finish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f"{self.address} {self.cep} {self.email}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        #return total_cost - total_cost * (self.discount / Decimal(100))
        return total_cost
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity