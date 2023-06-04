from products.models import Category, Product


def categories_and_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return {
        'categories': categories,
        'products': products
    }
