from django.db import models


class ContactForm(models.Model):
    """
    NEW MODEL
    Model for contact form
    """
    form_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class NewsletterSubscriber(models.Model):
    """
    NEW MODEL
    Newsletter form
    """
    email = models.EmailField(unique=True)
    agreed_to_tcs = models.BooleanField(default=False)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
