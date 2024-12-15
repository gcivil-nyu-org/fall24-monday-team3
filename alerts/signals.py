from django.db.models.signals import post_save
from django.dispatch import receiver
from rentals.models import ApartmentPost, Favorite
from alerts.models import PriceAlert
from alerts.utils import send_alert_email


@receiver(post_save, sender=ApartmentPost)
def check_price_drops_or_location_changes(sender, instance, created, **kwargs):
    """
    Trigger emails when:
    1. The price of an apartment post drops below the max price in a price alert.
    2. The location of the apartment post matches a price alert's location.
    """

    # Fetch all price alerts that match the post type and max price
    alerts = PriceAlert.objects.filter(
        post_type=instance.post_type,
        max_price__gte=instance.price,  # Match price within the alert's range
    )

    # Filter further by location (if the alert specifies one)
    matching_alerts = [
        alert
        for alert in alerts
        if not alert.location
        or alert.location.strip().lower() == instance.address.strip().lower()
    ]

    # Send alerts for matching price alerts
    for alert in matching_alerts:
        # Skip sending email to the user who created the post
        if alert.user == instance.user:
            continue
        # Check if the apartment post is a favorite for the user
        is_favorite = Favorite.objects.filter(user=alert.user, post=instance).exists()
        send_alert_email(alert.user, instance, is_favorite, is_updated=not created)


@receiver(post_save, sender=PriceAlert)
def check_alert_updates(sender, instance, **kwargs):
    """
    Trigger emails when:
    1. The max price in a price alert is updated.
    2. The location in a price alert is updated.
    """
    # Fetch apartment posts that match the updated alert
    matching_posts = ApartmentPost.objects.filter(
        post_type=instance.post_type,
        price__lte=instance.max_price,  # Within the updated max price
    )

    # If the alert specifies a location, filter by location
    if instance.location:
        matching_posts = matching_posts.filter(
            address__icontains=instance.location.strip()
        )

    # Send alerts for the matching apartment posts
    for post in matching_posts:
        is_favorite = post.favorites.filter(user=instance.user).exists()
        send_alert_email(instance.user, post, is_favorite, is_updated=True)
