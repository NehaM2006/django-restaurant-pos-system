from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    show = forms.BooleanField(
        label="Show Password",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "show-password"})
    )