# from django.contrib import admin
# from . models import Product
# # Register your models here.
# # admin.site.register(Product)

# class ProductAdmin(admin.ModelAdmin): # admin panel customize korte modeladmin use kori
#      list_display = ['product_name', 'price', 'category','stock' ,'created_date', 'modified_date', 'is_available']
     
#      prepopulated_fields = {'slug' : ('product_name',)}
     
# admin.site.register(Product, ProductAdmin)



from django.contrib import admin
from .models import Product, ReviewRating

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)