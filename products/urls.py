from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('categories/<int:category_id>/products/', views.category_products, name='category_products'),  # noqa
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),  # noqa
    path('review/<int:review_id>/toggle-authorization/', views.toggle_review_authorization, name='toggle_review_authorization'),  # noqa
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add/', views.add_product, name='add_product'),
]
