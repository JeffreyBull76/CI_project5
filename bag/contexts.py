from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    # Initialize variables
    bag_items = []
    total = 0
    product_count = 0

    # Get the bag from the session
    bag = request.session.get('bag', {})

    # Iterate through each item in the bag
    for item_id, item_data in bag.items():
        # Retrieve the corresponding product from the database
        product = get_object_or_404(Product, pk=item_id)

        # Calculate item subtotal and update total and product count
        total += item_data * product.price
        product_count += item_data

        # Add bag item details to the bag_items list
        bag_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'product': product,
        })

    # Calculate the delivery cost and grand total
    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    grand_total = delivery + total

    # Create a context dictionary with relevant data
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
