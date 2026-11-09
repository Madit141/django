from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from marketplace.models import Product, ProductType, Customer, Order, OrderItem, ProductImage
from marketplace.serializers import (
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    ProductTypeSerializer,
    ProductImageSerializer,
)

class ProductsViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return qs

        if user.is_superuser:
            user_filter = self.request.query_params.get("user")
            if user_filter:
                return qs.filter(user_id=user_filter)
            return qs

        return qs.filter(user=user)


class ProductTypesViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class CustomersViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrdersViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemsViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ProductImagesViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer