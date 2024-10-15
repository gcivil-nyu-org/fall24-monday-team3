from django.urls import path
from . import views
from .views import login_view,register_view
urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]
