# rentals/admin.py

from django.contrib import admin
from .models import ApartmentPost, ApartmentImage, Amenity

admin.site.register(ApartmentPost)
admin.site.register(ApartmentImage)
admin.site.register(Amenity)
