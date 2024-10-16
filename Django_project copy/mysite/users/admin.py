from django.contrib import admin
from .models import User  # Import your models

# Optionally create a custom admin class for the User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')  # Columns to display in the list view
    search_fields = ('username', 'email')  # Fields to enable search
    list_filter = ('is_active', 'is_staff')  # Filters for the list view

# Register the User model with the custom UserAdmin class
admin.site.register(User, UserAdmin)

# # Register the Group model with the default ModelAdmin (no customizations)
# admin.site.register(Group)
