from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404  # noqa
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a specified quantity of a product to the shopping bag.
    """

    # Retrieve the product and quantity from the request
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    # Retrieve the redirect URL and shopping bag from the session
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Add the product and quantity to the shopping bag
    if item_id in bag.keys():
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')  # noqa
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    # Update the shopping bag in the session
    request.session['bag'] = bag

    # Redirect to the specified URL
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specified product in the shopping bag.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    # Retrieve the shopping bag from the session
    bag = request.session.get('bag', {})

    # Adjust the quantity of the product in the shopping bag
    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')  # noqa
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    # Update the shopping bag in the session
    request.session['bag'] = bag

    # Redirect to the bag view
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the specified item from the shopping bag.
    """

    try:
        # Retrieve the product and bag from the session
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        # Remove the item from the bag & display a success message
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

        # Update the shopping bag in the session
        request.session['bag'] = bag

        # Return a success response
        return HttpResponse(status=200)

    except Exception as e:
        # Display an error message if an exception occurs
        messages.error(request, f'Error removing item: {e}')

        # Return an error response
        return HttpResponse(status=500)
