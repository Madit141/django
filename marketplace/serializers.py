from rest_framework import serializers

from marketplace.models import Product, ProductType, Customer, Order, OrderItem, ProductImage

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "quantity", "category", "image", "images", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"