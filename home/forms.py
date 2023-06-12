from django import forms
from .models import ContactForm


class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'comment']  # noqa
