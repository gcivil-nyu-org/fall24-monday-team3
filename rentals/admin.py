# rentals/admin.py

from django.contrib import admin
from .models import ApartmentPost, ApartmentImage, Amenity, Rating


class ApartmentPostAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "amenities",
    )  # Provides a horizontal filter for selecting multiple amenities


admin.site.register(ApartmentPost)
admin.site.register(ApartmentImage)
admin.site.register(Amenity)
admin.site.register(Rating)
