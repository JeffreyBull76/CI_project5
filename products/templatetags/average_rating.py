from django import template


register = template.Library()
# Creating an instance of the template library


@register.filter
def calculate_average_rating(reviews):
    """
    Custom filter for averaging the review scores of a product.
    When called it expects an object with a relevant 'rating' associated.

    Args:
        reviews (list): A list of review objects.

    Returns:
        float: The average rating rounded to one decimal place.
    """

    total_rating = sum(review.rating for review in reviews)
    # Calculate the total rating

    average_rating = total_rating / len(reviews) if reviews else 0
    # Calculate the average rating
    # or return 0 if the reviews list is empty

    return round(average_rating, 1)
    # Return the average rating rounded to one decimal place
