from django.shortcuts import render
from products.models import Category, Product


def index(request):
    """ View returns index page """
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home/index.html', context)
