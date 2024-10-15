from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ApartmentPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField()
    square_feet = models.PositiveIntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return self.title

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(ApartmentPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='apartment_images/')

    def __str__(self):
        return f"Image for {self.apartment.title}"
