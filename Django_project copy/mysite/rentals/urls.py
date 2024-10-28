# rentals/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_apartment_post, name="create_apartment_post"),
    path("", views.apartment_list, name="apartment_list"),
    path("apartment/<int:pk>/", views.apartment_detail, name="apartment_detail"),
    path("apartment/<int:pk>/edit/", views.update_apartment_post, name="update_apartment_post"),  # Update view
    path("apartment/<int:pk>/delete/", views.delete_apartment_post, name="delete_apartment_post"),  # Delete view
    path("<int:post_id>/rate/", views.rate_post, name="rate_post"),
    path("search/", views.search_apartments, name="search_apartments"),
    path("<int:post_id>/rate/clear/", views.clear_rating, name="clear_rating"),
    # You can add more URL patterns here, such as detail views
]
