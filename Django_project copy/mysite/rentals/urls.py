# rentals/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_apartment_post, name='create_apartment_post'),
    path('', views.apartment_list, name='apartment_list'),
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('<int:post_id>/rate/', views.rate_post, name='rate_post'),
    path('search/', views.search_apartments, name='search_apartments'),
    # You can add more URL patterns here, such as detail views
]
