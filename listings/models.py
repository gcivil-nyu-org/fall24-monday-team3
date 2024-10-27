from django.db import models

class Rental(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rental_images/', null=True, blank=True)
    location = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    apartment_type = models.CharField(max_length=50, choices=[
        ('studio', 'Studio'),
        ('1_bed', '1 Bed'),
        ('2_bed', '2 Bed'),
        ('3_bed', '3 Bed')
    ])
    sqft = models.IntegerField()
    amenities = models.TextField()

    def __str__(self):
        return self.title

