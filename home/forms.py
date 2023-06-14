from django import forms
from .models import ContactForm, NewsletterSubscriber


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


class NewsletterSignupForm(forms.ModelForm):
    """
    New form to handle newsletter subscription
    """
    agreed_to_tcs = forms.BooleanField(label='I agree to the terms and conditions')  # noqa

    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'agreed_to_tcs']

    def clean_email(self):
        email = self.cleaned_data['email']
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
