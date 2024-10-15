from django.db import models

# Create your models here.

from django.db import models

class Rental(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    apartment_type = models.CharField(max_length=50)
    sqft = models.IntegerField()
    amenities = models.TextField()

    def __str__(self):
        return self.title

