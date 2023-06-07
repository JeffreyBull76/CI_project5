from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Review
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
    product = get_object_or_404(Product, pk=product_id)

    is_reviewed = False
    if request.user.is_authenticated:
        is_reviewed = product.reviews.filter(user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated and not is_reviewed:  # noqa
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        print('Rating:', rating)
        print('Comment:', comment)
        review = Review(user=request.user, product=product, rating=rating, comment=comment)  # noqa
        # Validate the review object
        review.full_clean(validate_unique=False)
        review.save()
        product.reviews.add(review)
        # Redirect back to the same page after form submission
        return HttpResponseRedirect(request.path)

    # Fetch reviews associated with the product, newest first
    reviews = product.reviews.order_by('-id')

    context = {
        'product': product, 'is_reviewed': is_reviewed, 'reviews': reviews,
        }
    return render(request, 'products/product_detail.html', context)


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    categories = None

    context = {
        'products': products,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)
