from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import EmailVerificationToken, PendingEmailChange
from django.core import mail
import uuid
import json


class UserSignUpTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        self.User = get_user_model()

    def test_signup_page_loads(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_successful_signup(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123!",
            "password2": "testpass123!",
            "first_name": "Test",
            "last_name": "User",
            "bio": "Test bio",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)

        # Check user was created but not active
        user = self.User.objects.get(username="testuser")
        self.assertFalse(user.is_active)

        # Check verification email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Verify your RentSense account", mail.outbox[0].subject)

    def test_invalid_signup_missing_fields(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            # Missing required fields
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(username="testuser").exists())

    def test_invalid_signup_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123!",
            "password2": "differentpass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(username="testuser").exists())

    def test_duplicate_email_signup(self):
        # Create a user first
        self.User.objects.create_user(
            username="existing", email="test@example.com", password="testpass123!"
        )

        # Try to create another user with same email
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123!",
            "password2": "testpass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(username="testuser").exists())


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123!"
        )
        self.login_url = reverse("login")

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_successful_login(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123!"}
        )
        self.assertRedirects(response, reverse("home"))

    def test_invalid_login(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        # Check for the form's error messages
        form = response.context["form"]
        self.assertTrue(form.errors)  # Verify there are errors
        self.assertIn(
            "Please enter a correct username and password",
            form.errors.get("__all__")[0],
        )


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser", password="testpass123!")

    def test_profile_page_loads(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_edit_profile_without_email_change(self):
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "test@example.com",
            "bio": "Updated bio",
        }
        response = self.client.post(
            reverse("edit_profile"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_edit_profile_with_email_change(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "newemail@example.com",
            "bio": "Test bio",
            "email_changed": True,
        }
        response = self.client.post(
            reverse("edit_profile"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Check that old email is still active
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "test@example.com")

        # Check that pending email change was created
        pending_change = PendingEmailChange.objects.get(user=self.user)
        self.assertEqual(pending_change.new_email, "newemail@example.com")

    def test_edit_profile_duplicate_email(self):
        # Create another user with the email we'll try to use
        other_user = self.User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123!",
            first_name="Other",
            last_name="User",
            bio="Other user's bio",
        )

        # First test duplicate email
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "other@example.com",  # Try to use other user's email
            "bio": "Test bio",
            "email_changed": True,
        }
        response = self.client.post(
            reverse("edit_profile"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "This email is already in use.")

        # Verify the user's email hasn't changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "test@example.com")

        # Now test viewing other user's profile
        response = self.client.get(
            reverse("public_profile", kwargs={"username": "otheruser"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/public_profile.html")
        self.assertEqual(response.context["profile_user"], other_user)

        # Test sending a message to other user
        message_data = {
            "subject": "Test Message",
            "message": "Hello, this is a test message!",
        }
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "otheruser"}),
            data=json.dumps(message_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["success"])

        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Message")
        self.assertEqual(mail.outbox[0].to[0], other_user.email)

    def test_edit_profile_invalid_json(self):
        response = self.client.post(
            reverse("edit_profile"),
            data="invalid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["success"])


class EmailVerificationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            is_active=False,
        )
        self.verification_token = EmailVerificationToken.objects.create(user=self.user)

    def test_email_verification(self):
        response = self.client.get(
            reverse("verify_email", kwargs={"token": self.verification_token.token})
        )
        self.assertRedirects(response, reverse("login"))

        # Check user is now active
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # Check verification token is marked as verified
        self.verification_token.refresh_from_db()
        self.assertTrue(self.verification_token.is_verified)

    def test_invalid_verification_token(self):
        response = self.client.get(
            reverse("verify_email", kwargs={"token": uuid.uuid4()})
        )
        self.assertEqual(response.status_code, 404)

    def test_verify_already_verified_token(self):
        # First verification
        self.client.get(
            reverse("verify_email", kwargs={"token": self.verification_token.token})
        )

        # Try to verify again
        response = self.client.get(
            reverse("verify_email", kwargs={"token": self.verification_token.token})
        )
        self.assertEqual(response.status_code, 404)

    def test_verify_email_change(self):
        # Create a user and pending email change
        user = self.User.objects.create_user(
            username="testuser2", email="old@example.com", password="testpass123!"
        )
        pending_change = PendingEmailChange.objects.create(
            user=user, new_email="new@example.com"
        )

        # Login the user first
        self.client.login(username="testuser2", password="testpass123!")

        # Verify the email change
        response = self.client.get(
            reverse("verify_email_change", kwargs={"token": pending_change.token})
        )
        self.assertRedirects(response, reverse("profile"))

        # Check that email was updated
        user.refresh_from_db()
        self.assertEqual(user.email, "new@example.com")

        # Check that pending change was deleted
        self.assertFalse(
            PendingEmailChange.objects.filter(token=pending_change.token).exists()
        )


class PublicProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            first_name="Test",
            last_name="User",
            bio="Test bio",
        )

    def test_public_profile_view(self):
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.get(
            reverse("public_profile", kwargs={"username": "testuser"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/public_profile.html")
        self.assertEqual(response.context["profile_user"], self.user)

    def test_nonexistent_profile_view(self):
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.get(
            reverse("public_profile", kwargs={"username": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_profile_access(self):
        response = self.client.get(
            reverse("public_profile", kwargs={"username": "testuser"})
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('public_profile', kwargs={'username': 'testuser'})}",
        )


class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            first_name="Test",
            last_name="User",
            bio="Test bio",
        )

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Test User")

    def test_user_short_name(self):
        self.assertEqual(self.user.get_short_name(), "Test")


class EmailVerificationTokenTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123!"
        )
        self.token = EmailVerificationToken.objects.create(user=self.user)

    def test_token_str_method(self):
        self.assertEqual(str(self.token), f"Token for {self.user.email}")

    def test_token_creation(self):
        self.assertIsNotNone(self.token.token)
        self.assertFalse(self.token.is_verified)
        self.assertIsNotNone(self.token.created_at)


class PendingEmailChangeTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123!"
        )
        self.pending_change = PendingEmailChange.objects.create(
            user=self.user, new_email="new@example.com"
        )

    def test_pending_change_str_method(self):
        expected = (
            f"Email change for {self.user.username} to {self.pending_change.new_email}"
        )
        self.assertEqual(str(self.pending_change), expected)

    def test_token_generation(self):
        self.assertIsNotNone(self.pending_change.token)
        self.assertIsInstance(self.pending_change.token, uuid.UUID)


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            is_active=True,
        )
        self.client.login(username="testuser", password="testpass123!")

    def test_home_view_authenticated(self):
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/home.html")

    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/home.html")

    def test_send_user_email(self):
        data = {"subject": "Test Subject", "message": "Test Message"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Subject")

    def test_send_user_email_invalid_user(self):
        data = {"subject": "Test Subject", "message": "Test Message"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "nonexistent"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data["success"])

    def test_send_user_email_invalid_json(self):
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data="invalid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data["success"])

    def test_send_user_email_missing_fields(self):
        # Test missing subject
        data = {"message": "Test Message"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Missing subject or message")

        # Test missing message
        data = {"subject": "Test Subject"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Missing subject or message")

    def test_send_user_email_wrong_content_type(self):
        data = {"subject": "Test Subject", "message": "Test Message"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data=data,  # Not JSON
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(
            response_data["error"], "Content-Type must be application/json"
        )

    def test_send_user_email_unauthenticated(self):
        self.client.logout()
        data = {"subject": "Test Subject", "message": "Test Message"}
        response = self.client.post(
            reverse("send_user_email", kwargs={"username": "testuser"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('send_user_email', kwargs={'username': 'testuser'})}",
        )

    def test_edit_profile_with_empty_fields(self):
        data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "bio": "",
            "email_changed": False,
        }
        response = self.client.post(
            reverse("edit_profile"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["success"])

        # Verify fields weren't changed to empty strings
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(
            self.user.email, "test@example.com"
        )  # Email shouldn't be empty

    def test_edit_profile_unauthenticated(self):
        self.client.logout()
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "bio": "Test bio",
        }
        response = self.client.post(
            reverse("edit_profile"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('edit_profile')}"
        )

    def test_edit_profile_invalid_email(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email",
            "bio": "Test bio",
            "email_changed": True,
        }
        response = self.client.post(
            reverse("edit_profile"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Invalid email format")
