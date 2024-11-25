from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ApartmentPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Price of the apartment must be zero or higher.",
    )
    address = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    square_feet = models.PositiveIntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    average_rating = models.FloatField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    POST_TYPES = [
        ("APARTMENT", "Apartment"),
        ("ROOM", "Room"),
    ]
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default="APARTMENT")

    def __str__(self):
        return self.title


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        ApartmentPost, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(storage=S3Boto3Storage())

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


class Comment(models.Model):
    post = models.ForeignKey(
        ApartmentPost, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # New field to allow nested comments
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

    @property
    def is_reply(self):
        return self.parent is not None


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        "ApartmentPost", on_delete=models.CASCADE, related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.post.title}"
