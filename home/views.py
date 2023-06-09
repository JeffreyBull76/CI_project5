from django.shortcuts import render, redirect, get_object_or_404, reverse  # noqa
from products.models import Category, Product
from .forms import ContactFormModelForm, NewsletterSignupForm
from .models import ContactForm, NewsletterSubscriber
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def index(request):
    """ View returns index page """
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home/index.html', context)


def send_contact_email(data):
    """
    View to handle sending the contact form.
    """
    subject = "Website Inquiry"
    body = f"""
    First Name: {data['first_name']}
    Last Name: {data['last_name']}
    Email: {data['email']}
    Phone Number: {data['phone_number']}
    Comment: {data['comment']}
    """
    try:
        send_mail(
            subject,
            body,
            # Set the 'from' email
            'bullandsea@example.com',
            # Use the user's email as the sender
            [data['email']],
            fail_silently=False
        )
    # Header checking added despite not being needed for future use
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            # Perform field-level validation
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']

            if any(char.isdigit() for char in first_name):
                form.add_error('first_name', 'Only letters are allowed in the first name.')  # noqa
            if any(char.isdigit() for char in last_name):
                form.add_error('last_name', 'Only letters are allowed in the last name.')  # noqa
            if any(char.isalpha() for char in phone_number):
                form.add_error('phone_number', 'Only numbers are allowed in the phone number.')  # noqa

            if not form.errors:
                form.save()
                # Send email with form data using our view
                send_contact_email(form.cleaned_data)
                messages.success(request, 'Successfully sent message!')
                # Redirect to the success page
                return redirect('home')
    else:
        form = ContactFormModelForm()

    return render(request, 'home/contact_form.html', {'form': form})


# login required to prevent logged out access
@login_required
def contact_form_management_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    contact_forms = ContactForm.objects.all()

    # Count new messages
    new_messages_count = contact_forms.count()

    # Pass new_messages_count to the template context
    return render(request, 'home/contact_form_management.html', {
        'contact_forms': contact_forms,
        'new_messages_count': new_messages_count
    })


@login_required
def delete_message(request, message_id):
    """
    View to handle deleting contact form entries.
    """

    # prevent non superusers accessing this view
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    message = get_object_or_404(ContactForm, form_id=message_id)

    if request.method == 'POST':
        message.delete()

    messages.info(request, 'Message deleted!')
    # Redirect after deletion
    return redirect('contact_management')


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                form.save()
                messages.success(request, 'Signed up to newsletter!')
                return redirect('home')
            else:
                form.add_error('email', 'This email is already subscribed.')
    else:
        form = NewsletterSignupForm()
    return render(request, 'home/signup.html', {'form': form})
