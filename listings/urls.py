from django.urls import path
from . import views

urlpatterns = [
    path('', views.rental_list, name='rental_list'),
    path('create/', views.create_rental, name='create_rental'),
    path('<int:rental_id>/', views.rental_detail, name='rental_detail'),
    path('<int:rental_id>/update/', views.update_rental, name='update_rental'),
    path('<int:rental_id>/delete/', views.delete_rental, name='delete_rental'),
]
