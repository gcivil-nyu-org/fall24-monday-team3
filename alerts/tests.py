from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from alerts.models import PriceAlert
from rentals.models import ApartmentPost, Favorite
from django.core.exceptions import ValidationError


class PriceAlertModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="testuser", password="password123", email="random@test.com")

    @patch("alerts.utils.send_alert_email")
    def test_no_alert_for_users_own_post(self, mock_send_email):
        # Create a price alert
        alert = PriceAlert.objects.create(
            user=self.user,
            max_price=1500.00,
            property_type="APARTMENT",
        )

        # Create an apartment post by the same user with all required fields
        post = ApartmentPost.objects.create(
            user=self.user,
            price=1400.00,
            post_type="APARTMENT",
            address="New York",
            square_feet=600,
        )

        # Assert that no email was sent
        mock_send_email.assert_not_called()
