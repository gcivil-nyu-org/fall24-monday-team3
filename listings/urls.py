from django.urls import path
from . import views

urlpatterns = [
    path('rental/<int:rental_id>/detail/', views.rental_detail, name='rental_detail'),
    path('rental/<int:rental_id>/update/', views.update_rental, name='update_rental'),
    path('rental/<int:rental_id>/delete/', views.delete_rental, name='delete_rental'),
    path('rental/', views.rental_list, name='rental_list'),
]
