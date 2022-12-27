from django.db import models
from django.urls import reverse
from accounts.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from tinymce.models import HTMLField


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

class Image(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__ (self):
        return self.image.url

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    image = models.ManyToManyField(Image, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='like')
    deslike = models.ManyToManyField(User, blank=True, related_name='deslike')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = HTMLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return f'{self.category} {self.brand} {self.name}'

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.category, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.brand.name} {self.name}')
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(default='', max_length=600)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.product} on {1}'
