from django.contrib import admin
from .models import Category, Product, Brand, Image, Comment
from django import forms
from django.core.files.images import ImageFile



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'description']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('category','brand','name',)}


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         exclude = ['name']

#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     img = cleaned_data['image']
#     #     ok = ImageFile(img)
#     #     print (ok.width)
#     #     # if User.objects.filter(email__icontains=cleaned_data.get('email')).exists():
#     #     #     raise ValidationError(
#     #     #         self.error_messages["email_exists"],
#     #     #         code="email_exists",
#     #     #     )
#     #     return cleaned_data

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductForm

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)