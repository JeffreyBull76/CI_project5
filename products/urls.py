from django.urls import path
from . import views

urlpatterns = [
    path('categories/<int:category_id>/products/', views.category_products, name='category_products'),  # noqa
]
