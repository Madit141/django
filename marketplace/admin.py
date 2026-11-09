from django.contrib import admin

from marketplace.models import Product, ProductType, Customer, Order, OrderItem, Profile, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'category', 'user']
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']

@admin.register(ProductType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "phone", "photo"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "address"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "count"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "role"]

    def has_add_permission(self, request):
        return False