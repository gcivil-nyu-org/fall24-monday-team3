from django.db import models
from django.conf import settings


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoommatePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_location = models.CharField(max_length=255)
    hobbies = models.TextField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    description = models.TextField(default="No description provided")

    def __str__(self):
        return self.name


class RoommateImage(models.Model):
    roommate = models.ForeignKey(
        RoommatePost, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="roommate_images/")

    def __str__(self):
        return f"Image for {self.roommate.name}"


class Comment(models.Model):
    post = models.ForeignKey(
        RoommatePost, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roommate_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.post.name}"

    @property
    def is_reply(self):
        return self.parent is not None
