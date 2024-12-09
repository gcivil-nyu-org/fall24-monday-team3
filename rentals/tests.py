from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ApartmentPost, Rating
from django.contrib.messages import get_messages


class ApartmentPostOwnershipTest(TestCase):
    def setUp(self):
        # Create two test users
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(
            username="owner", password="testpass123", email="owner@test.com"
        )
        self.other_user = self.User.objects.create_user(
            username="other", password="testpass123", email="other@test.com"
        )

        # Create a test apartment post
        self.apartment = ApartmentPost.objects.create(
            user=self.owner,
            title="Test Apartment",
            post_type="APARTMENT",
            description="Test Description",
            price=1000.00,
            address="320 50th Street",
            bedrooms=2,
            square_feet=1000,
        )

        # Set up the test client
        self.client = Client()

    def test_owner_can_edit_post(self):
        # Log in as owner
        self.client.login(username="owner", password="testpass123")

        # Try to access edit page
        response = self.client.get(
            reverse("update_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Try to edit the post
        update_data = {
            "title": "Updated Title",
            "post_type": "APARTMENT",
            "description": "Updated Description",
            "price": 1200.00,
            "address": "320 50th Street",
            "bedrooms": 2,
            "square_feet": 1000,
        }
        response = self.client.post(
            reverse("update_apartment_post", kwargs={"pk": self.apartment.pk}),
            update_data,
        )

        # Check if redirect to detail page after successful update
        self.assertEqual(response.status_code, 302)

        # Verify the changes were saved
        updated_apartment = ApartmentPost.objects.get(pk=self.apartment.pk)
        self.assertEqual(updated_apartment.title, "Updated Title")
        self.assertEqual(updated_apartment.price, 1200.00)

    def test_non_owner_cannot_edit_post(self):
        # Log in as non-owner
        self.client.login(username="other", password="testpass123")

        # Try to access edit page
        response = self.client.get(
            reverse("update_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("don't have permission" in str(m) for m in messages))

    def test_owner_can_delete_post(self):
        # Log in as owner
        self.client.login(username="owner", password="testpass123")

        # Try to access delete page
        response = self.client.get(
            reverse("delete_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        self.assertEqual(response.status_code, 200)

        # Try to delete the post
        response = self.client.post(
            reverse("delete_apartment_post", kwargs={"pk": self.apartment.pk})
        )

        # Should redirect to apartment list after deletion
        self.assertEqual(response.status_code, 302)

        # Verify the post was deleted
        self.assertFalse(ApartmentPost.objects.filter(pk=self.apartment.pk).exists())

    def test_non_owner_cannot_delete_post(self):
        # Log in as non-owner
        self.client.login(username="other", password="testpass123")

        # Try to access delete page
        response = self.client.get(
            reverse("delete_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("don't have permission" in str(m) for m in messages))

        # Verify the post still exists
        self.assertTrue(ApartmentPost.objects.filter(pk=self.apartment.pk).exists())

    def test_unauthenticated_user_cannot_access_edit_delete(self):
        # Try to access edit page without logging in
        response = self.client.get(
            reverse("update_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))

        # Try to access delete page without logging in
        response = self.client.get(
            reverse("delete_apartment_post", kwargs={"pk": self.apartment.pk})
        )
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))

    def test_edit_delete_buttons_visibility(self):
        # Create test apartment detail URL
        detail_url = reverse("apartment_detail", kwargs={"pk": self.apartment.pk})

        # Test as owner
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)  # Check status code first
        self.assertContains(response, "Edit Listing")
        self.assertContains(response, "Delete Listing")

        # Test as non-owner
        self.client.login(username="other", password="testpass123")
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)  # Check status code first
        self.assertNotContains(response, "Edit Listing")
        self.assertNotContains(response, "Delete Listing")

        # Test as unauthenticated user
        self.client.logout()
        response = self.client.get(detail_url)
        # Check if redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))


class ApartmentRatingTests(TestCase):
    def setUp(self):
        # Create test users
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", password="testpass123", email="test@test.com"
        )

        # Create apartment owner
        self.owner = self.User.objects.create_user(
            username="owner", password="testpass123", email="owner@test.com"
        )

        # Create a test apartment post with owner
        self.apartment = ApartmentPost.objects.create(
            user=self.owner,  # Set the owner
            title="Test Apartment",
            description="Test Description",
            price=1000.00,
            address="123 Test St",
            bedrooms=2,
            square_feet=1000,
        )

        # Set up the test client
        self.client = Client()

    def test_rating_submission(self):
        # Log in the user
        self.client.login(username="testuser", password="testpass123")

        # Submit a rating
        response = self.client.post(
            reverse("rate_post", kwargs={"post_id": self.apartment.pk}), {"rating": 4}
        )

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if rating was saved
        rating = Rating.objects.get(post=self.apartment, user=self.user)
        self.assertEqual(rating.value, 4)

        # Check if average rating was updated
        self.apartment.refresh_from_db()
        self.assertEqual(self.apartment.average_rating, 4.0)

    def test_rating_update(self):
        # Log in the user
        self.client.login(username="testuser", password="testpass123")

        # Submit initial rating
        self.client.post(
            reverse("rate_post", kwargs={"post_id": self.apartment.pk}), {"rating": 4}
        )

        # Update the rating
        response = self.client.post(
            reverse("rate_post", kwargs={"post_id": self.apartment.pk}), {"rating": 5}
        )

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if rating was updated
        rating = Rating.objects.get(post=self.apartment, user=self.user)
        self.assertEqual(rating.value, 5)

        # Check if there's only one rating from this user
        self.assertEqual(
            Rating.objects.filter(post=self.apartment, user=self.user).count(), 1
        )

    def test_clear_rating(self):
        # Log in the user
        self.client.login(username="testuser", password="testpass123")

        # Submit initial rating
        self.client.post(
            reverse("rate_post", kwargs={"post_id": self.apartment.pk}), {"rating": 4}
        )

        # Clear the rating
        response = self.client.post(
            reverse("clear_rating", kwargs={"post_id": self.apartment.pk})
        )

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if rating was deleted
        self.assertEqual(
            Rating.objects.filter(post=self.apartment, user=self.user).count(), 0
        )
