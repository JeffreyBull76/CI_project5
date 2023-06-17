from home.models import ContactForm


def new_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        contact_forms = ContactForm.objects.all()
        new_messages_count = contact_forms.count()
    else:
        new_messages_count = 0

    return {'new_messages_count': new_messages_count}
