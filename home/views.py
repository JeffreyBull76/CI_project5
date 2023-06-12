from django.shortcuts import render, redirect
from products.models import Category, Product
from .forms import ContactFormModelForm

from django.shortcuts import render, redirect
from .forms import ContactFormModelForm
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
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email with form data
            send_contact_email(form.cleaned_data)
            # Redirect to the success page
            return redirect('home')
    else:
        form = ContactFormModelForm()
    return render(request, 'home/contact_form.html', {'form': form})
