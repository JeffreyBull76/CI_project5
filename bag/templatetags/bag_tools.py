from django import template


# Create an instance of Django's template library
register = template.Library()


# Define a custom template filter called 'calc_subtotal'
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    # Calculate the subtotal by multiplying the price and quantity
    return price * quantity
