from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import EmailVerificationToken, PendingEmailChange
from django.core import mail
import uuid

class UserSignUpTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.User = get_user_model()

    def test_signup_page_loads(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_successful_signup(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test bio'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check user was created but not active
        user = self.User.objects.get(username='testuser')
        self.assertFalse(user.is_active)
        
        # Check verification email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Verify your RentSense account', mail.outbox[0].subject)

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!'
        )
        self.login_url = reverse('login')

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_successful_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123!'
        })
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        # Check for the form's error messages
        form = response.context['form']
        self.assertTrue(form.errors)  # Verify there are errors
        self.assertIn(
            'Please enter a correct username and password',
            form.errors.get('__all__')[0]
        )

class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            first_name='Test',
            last_name='User'
        )
        self.client.login(username='testuser', password='testpass123!')

    def test_profile_page_loads(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_without_email_change(self):
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'test@example.com',
            'bio': 'Updated bio'
        }
        response = self.client.post(
            reverse('edit_profile'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_edit_profile_with_email_change(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'bio': 'Test bio',
            'email_changed': True
        }
        response = self.client.post(
            reverse('edit_profile'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that old email is still active
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')
        
        # Check that pending email change was created
        pending_change = PendingEmailChange.objects.get(user=self.user)
        self.assertEqual(pending_change.new_email, 'newemail@example.com')

class EmailVerificationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            is_active=False
        )
        self.verification_token = EmailVerificationToken.objects.create(user=self.user)

    def test_email_verification(self):
        response = self.client.get(
            reverse('verify_email', kwargs={'token': self.verification_token.token})
        )
        self.assertRedirects(response, reverse('login'))
        
        # Check user is now active
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        
        # Check verification token is marked as verified
        self.verification_token.refresh_from_db()
        self.assertTrue(self.verification_token.is_verified)

    def test_invalid_verification_token(self):
        response = self.client.get(
            reverse('verify_email', kwargs={'token': uuid.uuid4()})
        )
        self.assertEqual(response.status_code, 404)
