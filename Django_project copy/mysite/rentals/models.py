from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ApartmentPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="apartments"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField()
    square_feet = models.PositiveIntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        ApartmentPost, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="apartment_images/")

    def __str__(self):
        return f"Image for {self.apartment.title}"


class Rating(models.Model):
    post = models.ForeignKey(
        ApartmentPost, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings"
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s rating for {self.post.title}"
