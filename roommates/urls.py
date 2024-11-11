# roommates/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_roommate_post, name="create_roommate_post"),
    path("", views.roommate_list, name="roommate_list"),
    path("roommate/<int:pk>/", views.roommate_detail, name="roommate_detail"),
    path(
        "roommate/<int:pk>/edit/",
        views.update_roommate_post,
        name="update_roommate_post",
    ),  # Update view
    path(
        "roommate/<int:pk>/delete/",
        views.delete_roommate_post,
        name="delete_roommate_post",
    ),  # Delete view
    path("search/", views.search_roommates, name="search_roommates"),
    path(
        "roommate/<int:pk>/comment/",
        views.create_roommate_comment,
        name="create_roommate_comment",
    ),  # Create comment
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_roommate_comment",
    ),
    # You can add more URL patterns here, such as detail views
]
