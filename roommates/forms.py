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
            "age": forms.NumberInput(
                attrs={"class": "form-control", "min": 18, "max": 100}
            ),
            "gender": forms.TextInput(attrs={"class": "form-control"}),
            "budget": forms.NumberInput(attrs={"class": "form-control"}),
            "preferred_location": forms.TextInput(attrs={"class": "form-control"}),
            "hobbies": forms.Textarea(attrs={"class": "form-control"}),
            "amenities": CheckboxSelectMultiple(),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18 or age > 100:
            raise forms.ValidationError("Age must be between 18 and 100.")
        return age
    
    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if gender not in ["Male", "Female"]:
            raise forms.ValidationError("Gender must be 'male' or 'female'.")
        return gender


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



