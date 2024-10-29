from django.db import models
# from PIL import Image


class Rental(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="rental_images/", null=True, blank=True)
    location = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    apartment_type = models.CharField(max_length=50, blank=True, null=True)
    sqft = models.IntegerField()
    amenities = models.TextField()

    def __str__(self):
        return self.title
