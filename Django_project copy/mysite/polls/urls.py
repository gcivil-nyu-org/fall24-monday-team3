from django.urls import path
from . import views

app_name = 'polls'  # Add this line to create a namespace for your app

urlpatterns = [
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/rate/', views.rate_post, name='rate_post'),
]