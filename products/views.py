from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse


def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))  # noqa
    else:
        products = Product.objects.none()

    context = {
        'products': products,
        'search_query': query
    }

    return render(request, 'products/products.html', context)


def category_products(request, category_id):
    # Logic to retrieve the category and products
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category_id=category_id)

    context = {
        'category_name': category.get_friendly_name(),
        'products': products
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    # Logic to retrieve product details
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
