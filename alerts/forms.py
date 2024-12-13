from django import forms
from alerts.models import PriceAlert


class PriceAlertForm(forms.ModelForm):
    class Meta:
        model = PriceAlert
        fields = ["post_type", "max_price", "location"]
        labels = {
            "post_type": "Post Type",
            "max_price": "Maximum Price",
            "location": "Location(optional)",
        }
        widgets = {
            "post_type": forms.Select(attrs={"class": "form-control"}),
            "max_price": forms.NumberInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }
