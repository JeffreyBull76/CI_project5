from django.db import models


class ContactForm(models.Model):
    """
    Model for contact form
    """
    form_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
