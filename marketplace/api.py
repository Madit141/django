from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from marketplace.models import Product
from marketplace.serializers import ProductSerializers

class ProductsViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers