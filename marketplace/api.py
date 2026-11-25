from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, Min
from rest_framework import mixins, serializers
from rest_framework.decorators import action 
from rest_framework.response import Response

from marketplace.models import Product, ProductType, Customer, Order, OrderItem, ProductImage
from marketplace.serializers import (
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    ProductTypeSerializer,
    ProductImageSerializer,
    UserSerializer
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
        
        if not self.request.user.is_authenticated:
            return qs.none()

        if self.request.user.is_superuser:
            user_filter = self.request.query_params.get("user")
            if user_filter:
                return qs.filter(user=user_filter)
            return qs

        return qs.filter(user=self.request.user)


    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = self.get_queryset().aggregate(
            count=Count("*"),
            avg=Avg("quantity"),
            max=Max("quantity"),
            min=Min("quantity"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = ProductType.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Customer.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Order.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = OrderItem.objects.aggregate(
            total=Count("*"),
            avg=Avg("count"),
            max=Max("count"),
            min=Min("count"),
        )
        stats["count"] = stats["total"]
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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


class UsersViewset(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return User.objects.none()