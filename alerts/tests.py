from django.test import TestCase
from alerts.models import PriceAlert
from users.models import User
from django.core.exceptions import ValidationError


class PriceAlertModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_create_valid_price_alert(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            post_type="APARTMENT",
            location="New York",
        )
        self.assertEqual(alert.user, self.user)
        self.assertEqual(alert.max_price, 1000.00)
        self.assertEqual(alert.post_type, "APARTMENT")
        self.assertEqual(alert.location, "New York")

    def test_negative_max_price_validation(self):
        alert = PriceAlert(
            user=self.user,
            max_price=-100.00,
            post_type="APARTMENT",
            location="New York",
        )
        with self.assertRaises(ValidationError) as context:
            alert.clean()
        self.assertIn("Max price cannot be negative.", str(context.exception))

    def test_str_representation(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            post_type="ROOM",
            location="San Francisco",
        )
        expected_str = "testuser's Alert - Room - Max Price: 1000.0"
        self.assertEqual(str(alert), expected_str)

    def test_location_allows_null_and_blank(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            post_type="APARTMENT",
            location=None,  # Testing null location
        )
        self.assertIsNone(alert.location)
