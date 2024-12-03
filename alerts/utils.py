from django.core.mail import send_mail
from django.conf import settings
from alerts.models import Notification


def send_alert_email(user, post, is_favorite, is_updated=False):
    """
    Send an email for a price alert based on the user's preferences.
    """
    # Customize subject based on the trigger type
    if is_updated:
        subject = "Price Alert: Updated Matches Found!"
    else:
        subject = "Price Alert: Listing Matches Your Criteria!"

    # Customize email message if the post is a favorite
    if is_favorite:
        email_message = (
            f"Good news! Your favorite post at {post.address} is within your updated price alert range location! "
            f"The price is now ${post.price:.2f}."
        )
    else:
        email_message = (
            f"The {post.post_type.lower()} at {post.address} is now available for ${post.price:.2f}, "
            f"which matches your price alert."
        )

    # Create notification
    Notification.objects.create(
        recipient=user,
        sender=user,  # System notification, so sender is the same as recipient
        message=email_message,
    )

    # Send the email
    send_mail(
        subject=subject,
        message=f"Hi {user.username},\n\n{email_message}\n\nVisit RentSense to learn more!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
