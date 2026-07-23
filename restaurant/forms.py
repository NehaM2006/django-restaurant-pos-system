from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Review

class UserLoginForm(AuthenticationForm):
    show = forms.BooleanField(
        label="Show Password",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "show-password"})
    )
class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your review..."
                }
            ),
        }