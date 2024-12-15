# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from alerts.models import PriceAlert, Notification
from alerts.forms import PriceAlertForm
from rentals.models import ApartmentPost
from django.utils.cache import add_never_cache_headers
from django.contrib import messages
from alerts.utils import send_alert_email  # Import the shared function
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required(login_url="/users/login/")
def price_alerts(request):
    alerts = PriceAlert.objects.filter(user=request.user)
    response = render(request, "alerts/price_alerts.html", {"alerts": alerts})
    add_never_cache_headers(response)  # Prevent browser from caching the response
    return response


@login_required(login_url="/users/login/")
def add_price_alert(request):
    """
    Add a new price alert for the logged-in user.
    """
    if request.method == "POST":
        form = PriceAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user  # Associate the alert with the logged-in user
            alert.save()
            return redirect("price_alerts")  # Redirect back to the list of price alerts
    else:
        form = PriceAlertForm()

    return render(request, "alerts/add_price_alert.html", {"form": form})


@login_required(login_url="/users/login/")
def edit_price_alert(request, alert_id):
    """
    Edit an existing price alert for the logged-in user.
    """
    alert = get_object_or_404(
        PriceAlert, id=alert_id, user=request.user
    )  # Ensure the user owns the alert
    previous_max_price = alert.max_price  # Store the previous max price for comparison
    previous_location = alert.location  # Store the previous location for comparison

    if request.method == "POST":
        form = PriceAlertForm(request.POST, instance=alert)
        if form.is_valid():
            alert = form.save()
            # Check if the max price increased
            # Check if the max price or location changed
            location_changed = alert.location != previous_location
            max_price_increased = alert.max_price > previous_max_price

            if location_changed or max_price_increased:
                # Fetch existing apartment posts within the new range
                matching_posts = ApartmentPost.objects.filter(
                    post_type=alert.post_type,
                    price__lte=alert.max_price,  # Within the new max price
                    price__gt=previous_max_price,  # Exclude those already within the old range
                )

                # If location is updated, filter by the new location
                if alert.location:
                    matching_posts = matching_posts.filter(
                        address__icontains=alert.location
                    )

                # Send alerts for the matching posts
                for post in matching_posts:
                    is_favorite = post.favorites.filter(user=request.user).exists()
                    send_alert_email(
                        request.user,
                        post,
                        is_favorite,
                        is_updated=(max_price_increased or location_changed),
                    )  # Pass the is_updated flag

            messages.success(request, "Price alert updated successfully!")
            return redirect("price_alerts")
    else:
        form = PriceAlertForm(instance=alert)

    return render(
        request, "alerts/edit_price_alert.html", {"form": form, "alert": alert}
    )


@login_required(login_url="/users/login/")
def delete_price_alert(request, alert_id):
    alert = get_object_or_404(
        PriceAlert, id=alert_id, user=request.user
    )  # Ensure the user owns the alert
    alert.delete()
    return redirect("price_alerts")  # Redirect to the list of price alerts


@login_required
def get_notifications(request):
    current_user = request.user
    print(
        f"\nFetching notifications for user: {current_user.username} (ID: {current_user.id})"
    )

    # Get notifications ONLY where the current user is the RECIPIENT
    user_notifications = Notification.objects.filter(
        recipient_id=current_user.id
    ).order_by("-created_at")

    notifications_data = [
        {
            "id": n.id,
            "sender_name": n.sender.get_full_name() or n.sender.username,
            "message": n.message,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M"),
            "is_read": n.is_read,
        }
        for n in user_notifications
    ]

    unread_count = user_notifications.filter(is_read=False).count()

    response = JsonResponse(
        {"notifications": notifications_data, "unread_count": unread_count}
    )

    # Add cache control headers
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    # Ensure the notification belongs to the current user as recipient
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient_id=request.user.id,  # Explicitly check recipient_id
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})


@login_required
@require_POST
def mark_all_notifications_read(request):
    try:
        # Update only notifications where current user is recipient
        updated = Notification.objects.filter(
            recipient_id=request.user.id, is_read=False  # Explicitly check recipient_id
        ).update(is_read=True)
        print(
            f"Marked {updated} notifications as read for recipient {request.user.username}"
        )
        return JsonResponse({"success": True, "count": updated})
    except Exception as e:
        print(f"Error marking notifications as read: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)
