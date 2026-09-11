from django.shortcuts import render
from django.http import HttpResponse

from marketplace.models import Product 
from django.views.generic import TemplateView
from typing import Any

class ShowProductsView(TemplateView):
    template_name = "products/show_products.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()

        return context
    
