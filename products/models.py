from django.db import models
from django.urls import reverse
from accounts.models import User

class Brand(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
    
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('products:product_list_by_category', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return f'{self.category} {self.brand} {self.name} {self.description} {self.price}'

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])