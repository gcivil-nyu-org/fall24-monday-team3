# rentals/forms.py

from django import forms
from .models import ApartmentPost, ApartmentImage
from django.forms.widgets import CheckboxSelectMultiple
from .models import Comment


class ApartmentPostForm(forms.ModelForm):
    class Meta:
        model = ApartmentPost
        fields = [
            "post_type",
            "title",
            "description",
            "price",
            "address",
            "bedrooms",
            "square_feet",
            "amenities",
        ]
        widgets = {
            "post_type": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "square_feet": forms.NumberInput(attrs={"class": "form-control"}),
            "amenities": CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **qwargs):
        super().__init__(*args, **qwargs)
        self.fields['bedrooms'].help_text = 'Required for apartments; optional for rooms.'

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')
        bedrooms = cleaned_data.get('bedrooms')

        if post_type == 'APARTMENT':
            if bedrooms is None:
                self.add_error('bedrooms', 'This field is required for apartments.')
        return cleaned_data


class ApartmentImageForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
