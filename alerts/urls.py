from django.urls import path
from . import views

urlpatterns = [
    path("price-alerts/", views.price_alerts, name="price_alerts"),
    path("price-alerts/add/", views.add_price_alert, name="add_price_alert"),
    path(
        "price-alerts/edit/<int:alert_id>/",
        views.edit_price_alert,
        name="edit_price_alert",
    ),
    path(
        "price-alerts/delete/<int:alert_id>/",
        views.delete_price_alert,
        name="delete_price_alert",
    ),
    path("notifications/", views.get_notifications, name="get_notifications"),
    path(
        "notifications/mark-all-read/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
    path(
        "notifications/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
]
