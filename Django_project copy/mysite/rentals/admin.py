# rentals/admin.py

from django.contrib import admin
from .models import ApartmentPost, ApartmentImage, Amenity, Rating

admin.site.register(ApartmentPost)
admin.site.register(ApartmentImage)
admin.site.register(Amenity)
admin.site.register(Rating)
