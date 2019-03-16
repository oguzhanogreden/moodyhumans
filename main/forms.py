from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "password_repeat"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Passwords should match.")

