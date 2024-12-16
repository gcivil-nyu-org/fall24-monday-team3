from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import PriceAlert, Notification
from decimal import Decimal

User = get_user_model()


class AlertsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_price_alert_creation(self):
        """Test creating a price alert"""
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="Test Location",
        )
        self.assertEqual(
            str(alert), f"{self.user.username}'s Alert - Apartment - Max Price: 1000.0"
        )

    def test_price_alert_validation(self):
        """Test price alert validation"""
        with self.assertRaises(ValidationError):
            alert = PriceAlert(
                user=self.user, max_price=-100.00, property_type="APARTMENT"
            )
            alert.full_clean()

    def test_notification_creation(self):
        """Test creating a notification"""
        notification = Notification.objects.create(
            recipient=self.user, sender=self.user, message="Test notification"
        )
        self.assertFalse(notification.is_read)

    def test_notification_ordering(self):
        """Test notification ordering"""
        Notification.objects.create(
            recipient=self.user, sender=self.user, message="First notification"
        )
        second_notification = Notification.objects.create(
            recipient=self.user, sender=self.user, message="Second notification"
        )
        latest_notification = Notification.objects.first()
        self.assertEqual(latest_notification, second_notification)

    def test_price_alerts_view(self):
        """Test price alerts view"""
        response = self.client.get(reverse("price_alerts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "alerts/price_alerts.html")

    def test_add_price_alert_view(self):
        """Test adding a price alert"""
        data = {
            "max_price": "1500.00",
            "property_type": "APARTMENT",
            "location": "New Location",
        }
        response = self.client.post(reverse("add_price_alert"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(PriceAlert.objects.filter(location="New Location").exists())

    def test_unauthenticated_access(self):
        """Test access to views when not logged in"""
        self.client.logout()
        response = self.client.get(reverse("price_alerts"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))

    def test_get_notifications(self):
        """Test getting notifications"""
        Notification.objects.create(
            recipient=self.user, sender=self.user, message="Test notification"
        )
        response = self.client.get(reverse("get_notifications"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["notifications"]), 1)

    def test_mark_notification_read(self):
        """Test marking a notification as read"""
        notification = Notification.objects.create(
            recipient=self.user, sender=self.user, message="Test notification"
        )
        response = self.client.post(
            reverse("mark_notification_read", args=[notification.id])
        )
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_notifications_read(self):
        """Test marking all notifications as read"""
        Notification.objects.create(
            recipient=self.user, sender=self.user, message="Test 1"
        )
        Notification.objects.create(
            recipient=self.user, sender=self.user, message="Test 2"
        )
        response = self.client.post(reverse("mark_all_notifications_read"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(n.is_read for n in Notification.objects.all()))

    def test_price_alert_with_location(self):
        """Test creating a price alert with location"""
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="New York",
        )
        self.assertEqual(alert.location, "New York")

    def test_signals_price_drop(self):
        """Test signal when price drops below alert threshold"""
        from rentals.models import ApartmentPost

        # Create a price alert
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="Test Location",
        )

        # Create an apartment post that matches the alert criteria
        post = ApartmentPost.objects.create(
            user=self.user,
            title="Test Post",
            description="Test Description",
            price=900.00,
            post_type="APARTMENT",
            address="Test Location",
            square_feet=1000,
        )

        # Check if notification was created
        notification = Notification.objects.filter(
            recipient=self.user, message__contains=str(post.price)
        ).first()

        self.assertIsNotNone(notification)

    def test_utils_send_alert_email(self):
        """Test alert email sending utility"""
        from rentals.models import ApartmentPost
        from alerts.utils import send_alert_email

        # Create an apartment post
        post = ApartmentPost.objects.create(
            user=self.user,
            title="Test Post",
            description="Test Description",
            price=900.00,
            post_type="APARTMENT",
            address="Test Location",
            square_feet=1000,
        )

        # Test sending alert email
        send_alert_email(self.user, post, is_favorite=False)

        # Check if notification was created
        notification = Notification.objects.filter(
            recipient=self.user, message__contains="Test Location"
        ).first()

        self.assertIsNotNone(notification)

    def test_edit_price_alert_view(self):
        """Test editing a price alert"""
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="Old Location",
        )

        data = {
            "max_price": "1500.00",
            "property_type": "APARTMENT",
            "location": "New Location",
        }

        response = self.client.post(reverse("edit_price_alert", args=[alert.id]), data)

        self.assertEqual(response.status_code, 302)
        alert.refresh_from_db()
        self.assertEqual(alert.location, "New Location")
        self.assertEqual(float(alert.max_price), 1500.00)

    def test_delete_price_alert_view(self):
        """Test deleting a price alert"""
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="Test Location",
        )

        response = self.client.post(reverse("delete_price_alert", args=[alert.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(PriceAlert.objects.filter(id=alert.id).exists())
