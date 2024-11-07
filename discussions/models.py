# discussions/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='discussions'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='discussions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('discussion_detail', kwargs={'pk': self.pk})


class Reply(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name='replies'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'replies'

    def __str__(self):
        return f'Reply by {self.author} on {self.discussion.title}'


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name='votes'
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'discussion']

    def __str__(self):
        return f'{self.user} voted {self.value} on {self.discussion.title}'
