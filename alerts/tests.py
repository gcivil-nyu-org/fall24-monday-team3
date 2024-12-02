from django.test import TestCase
from django.contrib.auth.models import User
from django.core.mail import outbox
from rentals.models import ApartmentPost
from alerts.models import PriceAlert


class PriceAlertSignalTestCase(TestCase):

    def setUp(self):
        """
        Set up test data for the signal and alert functionality.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )

        # Create a price alert for the user
        self.alert = PriceAlert.objects.create(
            user=self.user, max_price=1500, property_type="APARTMENT"
        )

    def test_signal_sends_email_for_matching_price(self):
        """
        Test if the signal sends an email when an ApartmentPost matches a PriceAlert.
        """
        # Create an apartment post that matches the price alert
        post = ApartmentPost.objects.create(
            user=self.user,
            title="Test Apartment",
            description="Test description",
            price=1400,
            address="123 Test St",
            post_type="APARTMENT",
        )

        # Check the email outbox
        self.assertEqual(len(outbox), 1)  # Verify an email was sent
        email = outbox[0]  # Access the first email

        # Verify email content
        self.assertIn("Price Alert: Listing Matches Your Criteria!", email.subject)
        self.assertIn("Hi testuser,", email.body)
        self.assertIn(
            "The apartment at 123 Test St is now available for $1400.00", email.body
        )
        self.assertEqual(email.to, ["testuser@example.com"])

    def test_no_email_sent_for_non_matching_price(self):
        """
        Test that no email is sent if the ApartmentPost price exceeds the PriceAlert max price.
        """
        # Create an apartment post that does not match the price alert
        ApartmentPost.objects.create(
            user=self.user,
            title="Expensive Apartment",
            description="Test description",
            price=2000,
            address="456 Expensive St",
            post_type="APARTMENT",
        )

        # Check the email outbox
        self.assertEqual(len(outbox), 0)  # No email should be sent

    def test_no_email_sent_for_different_property_type(self):
        """
        Test that no email is sent if the property type does not match the PriceAlert.
        """
        # Create a room post (different property type)
        ApartmentPost.objects.create(
            user=self.user,
            title="Test Room",
            description="Test description",
            price=500,
            address="789 Room St",
            post_type="ROOM",
        )

        # Check the email outbox
        self.assertEqual(len(outbox), 0)  # No email should be sent
