from django.contrib import admin
from .models import ContactForm, NewsletterSubscriber


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    """
    Admin class for the ContactForm model.
    """
    pass


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'agreed_to_tcs', 'signup_date')
    list_filter = ('agreed_to_tcs', 'signup_date')
