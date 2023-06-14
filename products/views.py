from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Lower
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import ProductForm
from .models import Product, Category, Review


def search_products(request):
    """
    Allow searching from search field
    """

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
        messages.error(request, "You didn't enter any search criteria!")
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

    # Apply sorting if the sort parameter is 'average_rating'
    if sort == 'average_rating':
        if direction == 'desc':
            # Annotate average rating and sort in descending order
            products = products.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')  # noqa
        else:
            # Annotate average rating and sort in ascending order
            products = products.annotate(average_rating=Avg('review__rating')).order_by('average_rating')  # noqa

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
    """
    Returns items based on category
    """

    # Retrieve the category object
    category = Category.objects.get(id=category_id)

    # Retrieve the products for the given category
    products = Product.objects.filter(category_id=category_id)

    # Initialize variables for sorting
    sort = None
    direction = None

    # Check if there are query parameters in the request
    if request.GET:
        # Check if 'sort' parameter is present
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # Sort the products by price
            if sortkey == 'price':
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = '-price'  # Sort in descending order
                products = products.order_by(sortkey)

            # Sort the products by average rating
            elif sortkey == 'average_rating':
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                if direction == 'desc':
                    # Annotate average rating and sort in descending order
                    products = products.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')  # noqa
                else:
                    # Annotate average rating and sort in ascending order
                    products = products.annotate(average_rating=Avg('review__rating')).order_by('average_rating')  # noqa

    # Create the current sorting string for display
    current_sorting = f'{sort}_{direction}'

    # Prepare the context for rendering the template
    context = {
        'category_name': category.get_friendly_name(),
        'products': products,
        'current_sorting': current_sorting,
    }

    # Render the template with the context
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    View function to display the details of a specific product.
    Allows authenticated users to add reviews for the product.
    """
    product = get_object_or_404(Product, pk=product_id)

    # Check if the current user has already reviewed the product
    is_reviewed = False
    if request.user.is_authenticated:
        is_reviewed = product.reviews.filter(user=request.user).exists()

    # Handle the form submission for adding a review
    if request.method == 'POST' and request.user.is_authenticated and not is_reviewed:  # noqa
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        # Create a new Review object
        review = Review(user=request.user, product=product, rating=rating, comment=comment)  # noqa

        # Validate the review object
        review.full_clean(validate_unique=False)

        # Save the review to the database and associate it with the product
        review.save()
        product.reviews.add(review)

        # Display a success message
        messages.info(request, 'Review added successfully!')

        # Redirect back to the same page after form submission
        return HttpResponseRedirect(request.path)

    # Fetch reviews associated with the product, ordered by the newest first
    reviews = product.reviews.order_by('-id')

    # Prepare the context data for the template
    context = {
        'product': product,
        'is_reviewed': is_reviewed,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    categories = Category.objects.all()

    # Initialize variables for sorting
    sort = None
    direction = None

    # Check if there are query parameters in the request
    if request.GET:
        # Check if 'sort' parameter is present
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # Sort the products by price
            if sortkey == 'price':
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = '-price'  # Sort in descending order
                products = products.order_by(sortkey)

            # Sort the products by average rating
            elif sortkey == 'average_rating':
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                if direction == 'desc':
                    # Annotate average rating and sort in descending order
                    products = products.annotate(average_rating=Avg('review__rating')).order_by('-average_rating')  # noqa
                else:
                    # Annotate average rating and sort in ascending order
                    products = products.annotate(average_rating=Avg('review__rating')).order_by('average_rating')  # noqa

    # Create the current sorting string for display
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


@login_required
@require_POST
def delete_review(request, review_id):
    """
    View function to delete reviews.
    Only superusers (store owners) can perform this action.
    """

    # Retrieve the review object based on the given review_id
    review = get_object_or_404(Review, pk=review_id)

    messages.info(request, 'Review deleted successfully!')
    review.delete()

    # Redirect to the product detail page
    return redirect('product_detail', product_id=review.product.pk)


@login_required
def toggle_review_authorization(request, review_id):
    """
    View function to toggle the authorization status of a review.
    Only superusers (store owners) can perform this action.
    """
    if not request.user.is_superuser:
        # Check if the current user is a superuser (store owner)
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    # Retrieve the review object based on the given review_id
    review = get_object_or_404(Review, pk=review_id)

    # Toggle the is_authorized field of the review between True and False
    review.is_authorized = not review.is_authorized
    review.save()

    if review.is_authorized:
        messages.info(request, 'The review has been authorized!')
    else:
        messages.info(request, 'The review has been unauthorized!')

    # Redirect to the product detail page of the review's associated product
    return HttpResponseRedirect(reverse_lazy('product_detail', args=[review.product.pk]))  # noqa


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')  # noqa
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')  # noqa
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
