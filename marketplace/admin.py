from django.contrib import admin

from marketplace.models import Product, ProductType

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'category']

@admin.register(ProductType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
