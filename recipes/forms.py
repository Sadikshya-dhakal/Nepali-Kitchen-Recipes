from django import forms
from recipes.models import Contact
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
