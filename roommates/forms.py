# rentals/forms.py

from django import forms
from .models import RoommatePost, RoommateImage, Comment
from django.forms.widgets import CheckboxSelectMultiple


class RoommatePostForm(forms.ModelForm):
    class Meta:
        model = RoommatePost
        fields = [
            "name",
            "age",
            "gender",
            "budget",
            "preferred_location",
            "hobbies",
            "amenities",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.TextInput(attrs={"class": "form-control"}),
            "budget": forms.NumberInput(attrs={"class": "form-control"}),
            "preferred_location": forms.TextInput(attrs={"class": "form-control"}),
            "hobbies": forms.Textarea(attrs={"class": "form-control"}),
            "amenities": CheckboxSelectMultiple(),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class RoommateImageForm(forms.ModelForm):
    class Meta:
        model = RoommateImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
