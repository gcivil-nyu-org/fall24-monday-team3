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
    if created:
        return  # Skip newly created posts; only check updates

    print(f"Signal triggered for ApartmentPost: {instance}, Price: {instance.price}")

    # Fetch active alerts that match the property type and max price
    alerts = PriceAlert.objects.filter(
        property_type=instance.post_type,
        max_price__gte=instance.price,
    )
    print(f"Matching alerts found: {alerts.count()}")

    # Filter further by location if specified in the alert
    matching_alerts = [
        alert
        for alert in alerts
        if not alert.location  # No location specified in the alert
        or alert.location.strip().lower() in instance.address.strip().lower()
    ]

    print(f"Final matching alerts after location filtering: {len(matching_alerts)}")

    # Send email for each matching alert
    for alert in matching_alerts:
        # Skip if the user owns the listing
        if instance.user == alert.user:
            print(f"Skipping alert for user {alert.user.email}, owns the listing.")
            continue

        # Check if the post is a favorite for the alert's user
        is_favorite = Favorite.objects.filter(user=alert.user, post=instance).exists()

        try:
            send_alert_email(alert.user, instance, is_favorite)
            print(f"Email sent to {alert.user.email} for ApartmentPost {instance.id}")
        except Exception as e:
            print(f"Error sending email to {alert.user.email}: {str(e)}")
