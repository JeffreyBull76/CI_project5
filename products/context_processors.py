from products.models import Category, Product


def categories_and_products(request):
    """
    Context processor to provide categories and products data across all apps.
    """
    categories = Category.objects.all()
    products = Product.objects.all()
    return {
        'categories': categories,
        'products': products
    }
