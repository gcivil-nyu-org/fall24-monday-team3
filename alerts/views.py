# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from alerts.models import PriceAlert
from alerts.forms import PriceAlertForm
from rentals.models import ApartmentPost
from django.utils.cache import add_never_cache_headers
from django.contrib import messages
from alerts.utils import send_alert_email  # Import the shared function


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
                    post_type=alert.property_type,
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
