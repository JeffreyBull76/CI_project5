from django.shortcuts import render
from .models import Product


def category_products(request, category_id):
    # Logic to retrieve products for the given category_id
    products = Product.objects.filter(category_id=category_id)

    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)
