from django.test import TestCase
from .forms import ApartmentPostForm
from .models import ApartmentPost


class ApartmentPostFormTests(TestCase):
    def test_apartment_post_form_valid(self):
        form_data = {
            'title': 'Test Apartment',
            'description': 'A nice place to live',
            'price': 1000,
            'address': '123 Main St',
            'bedrooms': 2,
            'square_feet': 850,
            'amenities': []  # Adjust as needed for your model
        }
        form = ApartmentPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    
    def test_apartment_post_form_invalid(self):
        form_data = {
            'title': '',
            'description': 'A nice place to live',
            'price': 1000,
            'address': '123 Main St',
            'bedrooms': 2,
            'square_feet': 850,
            'amenities': []  # Adjust as needed for your model
        }
        form = ApartmentPostForm(data=form_data)
        self.assertFalse(form.is_valid())


class ApartmentRatingTests(TestCase):
    def setUp(self):
        self.apartment = ApartmentPost.objects.create(
            title="Test Apartment",
            price=1000,
            average_rating=0,
            bedrooms=2,
            square_feet=850
        )

    def test_rating_submission(self):
        # Simulate a rating submission
        self.apartment.submit_rating(4)
        self.assertEqual(self.apartment.average_rating, 4)
