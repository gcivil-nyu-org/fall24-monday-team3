from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['title', 'description', 'price', 'image', 'location', 'zip_code', 'apartment_type', 'sqft', 'amenities']
