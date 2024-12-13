from django.db import models
from users.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class PriceAlert(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ("APARTMENT", "Apartment"),
        ("ROOM", "Room"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    post_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    location = models.CharField(
        max_length=255, blank=True, null=True
    )  # New field for location

    def clean(self):
        if self.max_price < 0:
            raise ValidationError("Max price cannot be negative.")

    def __str__(self):
        return f"{self.user.username}'s Alert - {self.post_type.title()} - Max Price: {self.max_price}"
