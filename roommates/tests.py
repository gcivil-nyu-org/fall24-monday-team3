from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import RoommatePost, Comment

# Create your tests here.

class RoommatePostOwnershipTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(
            username="owner", password="testpass123", email="owner@test.com"
        )
        self.other_user = self.User.objects.create_user(
            username="other", password="testpass123", email="other@test.com"
        )
        self.roommate_post = RoommatePost.objects.create(
            user=self.owner,
            name="Test Roommate",
            age=25,
            gender="Male",
            budget=500.00,
            preferred_location="Test Location",
            hobbies="Reading, Hiking",
            description="Looking for a roommate",
        )
        self.client = Client()

    def test_owner_can_edit_post(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(
            reverse("update_roommate_post", kwargs={"pk": self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_edit_post(self):
        self.client.login(username="other", password="testpass123")
        response = self.client.get(
            reverse("update_roommate_post", kwargs={"pk": self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user_cannot_access_edit_delete(self):
        response = self.client.get(
            reverse("update_roommate_post", kwargs={"pk": self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/users/login/"))

    def test_comment_submission(self):
        self.client.login(username="other", password="testpass123")
        response = self.client.post(
            reverse("create_roommate_comment", kwargs={"pk": self.roommate_post.pk}),
            {"content": "This is a test comment."}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.roommate_post).exists())
