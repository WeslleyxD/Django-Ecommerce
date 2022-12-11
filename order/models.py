from django.db import models
from perfil.models import Perfil
from products.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, db_index=True)
    finish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.address

    # def get_absolute_url(self):
    #     return reverse('products:product_detail', args=[self.id, self.slug])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity