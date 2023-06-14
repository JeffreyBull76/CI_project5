from django import forms
from .models import ContactForm


class ContactFormModelForm(forms.ModelForm):
    """
    ModelForm class for the ContactForm model.
    """

    class Meta:
        """
        Meta class specifying the model and form fields.
        """

        model = ContactForm
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'comment']  # noqa
