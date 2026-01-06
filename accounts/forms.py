from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User




class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Password",
        })
    )



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Enter your email",
        })
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Choose a username",
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Enter password",
        })
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500",
            "placeholder": "Confirm password",
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
