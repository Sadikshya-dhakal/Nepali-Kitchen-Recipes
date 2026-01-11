from django import forms
from recipes.models import Contact, NewsletterSubscription
from django.core.validators import RegexValidator

class ContactForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="Enter a valid phone number (digits only)."
            )
        ]
    )

    class Meta:
        model = Contact
        fields = "__all__"

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = "__all__"