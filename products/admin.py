from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image',
        'display_reviews',  # Add custom method here
    )
    ordering = ('sku',)

    def display_reviews(self, obj):
        reviews = obj.reviews.all()
        return ", ".join([f"{review.user.username} ({review.rating})" for review in reviews])  # noqa

    display_reviews.short_description = 'Reviews'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'rating',
    )


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
