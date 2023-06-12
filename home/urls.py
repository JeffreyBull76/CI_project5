from django.urls import path
from . import views
from .views import contact_form_management_view

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact_form_view, name='contact'),
    path('contact-management/', contact_form_management_view, name='contact_management'),  # noqa
    path('contact-management/delete/<int:message_id>/', views.delete_message, name='delete_message'),  # noqa
]
