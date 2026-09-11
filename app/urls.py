"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from marketplace.views import ShowProductsView
from marketplace.api import (
    CustomersViewset,
    OrderItemsViewset,
    OrdersViewset,
    ProductsViewset,
    ProductTypesViewset,
)

router = DefaultRouter()
router.register("products", ProductsViewset, basename="products")
router.register("product-types", ProductTypesViewset, basename="product-types")
router.register("customers", CustomersViewset, basename="customers")
router.register("orders", OrdersViewset, basename="orders")
router.register("order-items", OrderItemsViewset, basename="order-items")

urlpatterns = [
    path('', ShowProductsView.as_view(), name='product_list'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
