# rentals/admin.py

from django.contrib import admin
from .models import RoommatePost, RoommateImage, Amenity, Comment


class RoommatePostAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "amenities",
    )  # Provides a horizontal filter for selecting multiple amenities


admin.site.register(RoommatePost, RoommatePostAdmin)
admin.site.register(RoommateImage)
admin.site.register(Amenity)
admin.site.register(Comment)


