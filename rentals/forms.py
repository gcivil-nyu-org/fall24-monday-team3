# rentals/forms.py

from django import forms
from .models import ApartmentPost, ApartmentImage
from django.forms.widgets import CheckboxSelectMultiple


class ApartmentPostForm(forms.ModelForm):
    class Meta:
        model = ApartmentPost
        fields = [
            "title",
            "description",
            "price",
            "address",
            "bedrooms",
            "square_feet",
            "amenities",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "square_feet": forms.NumberInput(attrs={"class": "form-control"}),
            "amenities": CheckboxSelectMultiple(),
        }


class ApartmentImageForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }
