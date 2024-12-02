from django import forms
from alerts.models import PriceAlert


class PriceAlertForm(forms.ModelForm):
    class Meta:
        model = PriceAlert
        fields = ["property_type", "max_price", "location"]
        labels = {
            "property_type": "Property Type",
            "max_price": "Maximum Price",
            "location": "Location(optional)",
        }
        widgets = {
            "property_type": forms.Select(attrs={"class": "form-control"}),
            "max_price": forms.NumberInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }
