from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from alerts.models import PriceAlert
from rentals.models import ApartmentPost, Favorite
from django.core.exceptions import ValidationError

User = get_user_model()  # Dynamically fetch the User model

class PriceAlertModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="testuser", password="password123", email="random@test.com")



    def test_create_valid_price_alert(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location="New York",
        )
        self.assertEqual(alert.user, self.user)
        self.assertEqual(alert.max_price, 1000.00)
        self.assertEqual(alert.property_type, "APARTMENT")
        self.assertEqual(alert.location, "New York")

    def test_negative_max_price_validation(self):
        alert = PriceAlert(
            user=self.user,
            max_price=-100.00,
            property_type="APARTMENT",
            location="New York",
        )
        with self.assertRaises(ValidationError) as context:
            alert.clean()
        self.assertIn("Max price cannot be negative.", str(context.exception))

    def test_str_representation(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="ROOM",
            location="San Francisco",
        )
        expected_str = "testuser's Alert - Room - Max Price: 1000.0"
        self.assertEqual(str(alert), expected_str)

    def test_location_allows_null_and_blank(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1000.00,
            property_type="APARTMENT",
            location=None,  # Testing null location
        )
        self.assertIsNone(alert.location)



class SignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.alert = PriceAlert.objects.create(
            user=self.user,
            property_type='apartment',
            max_price=1000,
            location='Downtown',
        )
        self.apartment = ApartmentPost.objects.create(
            user=User.objects.create_user(username='owner', password='ownerpass'),
            post_type='apartment',
            price=1200,
            address='123 Downtown Street',
            square_feet=500,
        )


    @patch('alerts.signals.send_alert_email')
    def test_location_filtering(self, mock_send_email):
        # Change location in the alert to a non-matching one
        self.alert.location = "Non-Matching Location"
        self.alert.save()

        # Reduce the price of the listing
        self.apartment.price = 800
        self.apartment.save()

        # Assert that no email is sent
        mock_send_email.assert_not_called()

    @patch('alerts.signals.send_alert_email')
    def test_favorite_post_email(self, mock_send_email):
        # Mark the post as favorite for the alert user
        Favorite.objects.create(user=self.user, post=self.apartment)

        # Reduce the price
        self.apartment.price = 950
        self.apartment.save()

        # Check that the email mentions the favorite status
        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        print(f"Mock call args: {kwargs}")  # Add this line for debugging
        self.assertTrue(kwargs.get('is_favorite'))