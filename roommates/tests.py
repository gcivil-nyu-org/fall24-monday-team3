from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import RoommatePost, Comment, Favorite, Amenity
from .forms import RoommatePostForm, CommentForm
from decimal import Decimal

class RoommatePostModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", 
            password="testpass123",
            email="test@test.com"
        )
        self.amenity = Amenity.objects.create(name="WiFi")
        self.roommate_post = RoommatePost.objects.create(
            user=self.user,
            name="Test Roommate",
            age=25,
            gender="Male",
            budget=1000.00,
            preferred_location="Test Location",
            hobbies="Reading",
            description="Test description"
        )
        self.roommate_post.amenities.add(self.amenity)

    def test_roommate_post_str(self):
        self.assertEqual(str(self.roommate_post), "Test Roommate")

    def test_amenity_str(self):
        self.assertEqual(str(self.amenity), "WiFi")

    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.roommate_post,
            user=self.user,
            content="Test comment"
        )
        expected = f"Comment by {self.user} on {self.roommate_post.name}"
        self.assertEqual(str(comment), expected)

    def test_favorite_str(self):
        favorite = Favorite.objects.create(
            user=self.user,
            post=self.roommate_post
        )
        expected = f"{self.user.username}'s favorite: {self.roommate_post.name}"
        self.assertEqual(str(favorite), expected)

    def test_comment_is_reply(self):
        parent_comment = Comment.objects.create(
            post=self.roommate_post,
            user=self.user,
            content="Parent comment"
        )
        reply = Comment.objects.create(
            post=self.roommate_post,
            user=self.user,
            content="Reply comment",
            parent=parent_comment
        )
        self.assertTrue(reply.is_reply)
        self.assertFalse(parent_comment.is_reply)

class RoommateFormTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", 
            password="testpass123"
        )

    def test_valid_roommate_form(self):
        form_data = {
            'name': 'Test Name',
            'age': 25,
            'gender': 'Male',
            'budget': 1000.00,
            'preferred_location': 'Test Location',
            'hobbies': 'Reading',
            'description': 'Test description'
        }
        form = RoommatePostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_roommate_form(self):
        form_data = {
            'name': '',  # Required field
            'age': 15,   # Too young
            'gender': 'Invalid',
            'budget': -100,  # Negative budget
            'preferred_location': '',
            'hobbies': ''
        }
        form = RoommatePostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('age', form.errors)
        self.assertIn('gender', form.errors)

    def test_comment_form(self):
        form = CommentForm(data={'content': 'Test comment'})
        self.assertTrue(form.is_valid())

class RoommateViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", 
            password="testpass123",
            email="test@test.com"
        )
        self.roommate_post = RoommatePost.objects.create(
            user=self.user,
            name="Test Roommate",
            age=25,
            gender="Male",
            budget=1000.00,
            preferred_location="Test Location",
            hobbies="Reading",
            description="Test description"
        )

    def test_roommate_list_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('roommate_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roommates/roommate_list.html')

    def test_roommate_list_view_with_search(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('roommate_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roommates/roommate_list.html')

    def test_roommate_detail_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse('roommate_detail', kwargs={'pk': self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roommates/roommate_detail.html')

    def test_update_roommate_post(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse('update_roommate_post', kwargs={'pk': self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_roommate_post(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse('delete_roommate_post', kwargs={'pk': self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_update(self):
        other_user = self.User.objects.create_user(
            username="other", 
            password="testpass123"
        )
        self.client.login(username="other", password="testpass123")
        response = self.client.get(
            reverse('update_roommate_post', kwargs={'pk': self.roommate_post.pk})
        )
        self.assertEqual(response.status_code, 302)

class CommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", 
            password="testpass123"
        )
        self.roommate_post = RoommatePost.objects.create(
            user=self.user,
            name="Test Roommate",
            age=25,
            gender="Male",
            budget=1000.00,
            preferred_location="Test Location",
            hobbies="Reading"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_create_comment(self):
        response = self.client.post(
            reverse('create_roommate_comment', kwargs={'pk': self.roommate_post.pk}),
            {'content': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_reply(self):
        parent_comment = Comment.objects.create(
            post=self.roommate_post,
            user=self.user,
            content="Parent comment"
        )
        reply = Comment.objects.create(
            post=self.roommate_post,
            user=self.user,
            content="Reply comment",
            parent=parent_comment
        )
        self.assertTrue(reply.is_reply)
        self.assertFalse(parent_comment.is_reply)
