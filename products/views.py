from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse


def search_products(request):
    # Retrieve the search query from the GET parameters
    query = request.GET.get('q')

    if query:
        # Split the search query into individual search terms
        search_terms = query.split()

        # Filter products based on the first search term
        products = Product.objects.filter(
            Q(name__icontains=search_terms[0]) | Q(description__icontains=search_terms[0])  # noqa
        )

        # Filter products based on the remaining search terms using OR operator
        for term in search_terms[1:]:
            products |= Product.objects.filter(
                Q(name__icontains=term) | Q(description__icontains=term)
            )
    else:
        # If no search query is provided, return an empty queryset
        products = Product.objects.none()

    # Retrieve the sorting parameters from the GET parameters
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')

    # Apply sorting if the sort parameter is 'price'
    if sort == 'price':
        if direction == 'desc':
            # Sort products by descending price
            products = products.order_by('-price')
        else:
            # Sort products by ascending price
            products = products.order_by('price')

    # Create a string representing the current sorting criterion and direction
    current_sorting = f'{sort}_{direction}'

    # Prepare the context to be passed to the template
    context = {
        'products': products,
        'search_query': query,
        'current_sorting': current_sorting
    }

    # Render the template with the provided context
    return render(request, 'products/products.html', context)


def category_products(request, category_id):
    # Logic to retrieve the category and products
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category_id=category_id)
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'price':
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = '-price'
                products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'category_name': category.get_friendly_name(),
        'products': products,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    # Logic to retrieve product details
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
