from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51N59fdIHUuv4NymJanD3n8dpT9HBMCFXX6NW0v3TmO2FzIlPjGZdfuqZtsss9z9fl7cDFFGBzlVPRdCdWyM3FWRi00Mp341qHC',  # noqa
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
