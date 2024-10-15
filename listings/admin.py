from django.contrib import admin

# Register your models here.
from .models import Rental

# Register the Rental model so it's visible in the admin site
admin.site.register(Rental)
