# rentals/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_apartment_post, name="create_apartment_post"),
    path("", views.apartment_list, name="apartment_list"),
    path("apartment/<int:pk>/", views.apartment_detail, name="apartment_detail"),
    path(
        "apartment/<int:pk>/edit/",
        views.update_apartment_post,
        name="update_apartment_post",
    ),  # Update view
    path(
        "apartment/<int:pk>/delete/",
        views.delete_apartment_post,
        name="delete_apartment_post",
    ),  # Delete view
    path("<int:post_id>/rate/", views.rate_post, name="rate_post"),
    path("<int:post_id>/rate/clear/", views.clear_rating, name="clear_rating"),
    path(
        "apartment/<int:pk>/comment/",
        views.create_apartment_comment,
        name="create_apartment_comment",
    ),  # Create apartment comment
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_apartment_comment,
        name="delete_apartment_comment",
    ),
    path("search/", views.search_apartments, name="search_apartments"),
    path("apartment/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("apartment/<int:pk>/rate/", views.rate_apartment, name="rate_apartment"),
    path(
        "apartment/<int:pk>/clear-rating/",
        views.clear_apartment_rating,
        name="clear_apartment_rating",
    ),
    path("apartment-data/", views.apartment_data, name='apartment-data'),
    path("property-map/", views.property_map_view, name='property_map'),
]
