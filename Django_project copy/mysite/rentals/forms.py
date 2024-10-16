# rentals/forms.py

from django import forms
from .models import ApartmentPost, ApartmentImage

class ApartmentPostForm(forms.ModelForm):
    class Meta:
        model = ApartmentPost
        fields = [
            'title', 'description', 'price', 'address',
            'bedrooms', 'square_feet', 'amenities'
        ]

class ApartmentImageForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    class Meta:
        model = ApartmentImage
        fields = ['image']
