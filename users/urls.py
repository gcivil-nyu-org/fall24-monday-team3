from django.urls import path
from . import views
from .views import login_view, register_view, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
