from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Post(models.Model):
    content = models.TextField()
    average_rating = models.FloatField(default=0)

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])