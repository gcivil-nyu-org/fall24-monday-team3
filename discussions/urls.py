# discussions/urls.py
from django.urls import path
from . import views


app_name = 'discussions'

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('new/', views.discussion_create, name='discussion_create'),
    path('<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('<int:pk>/vote/', views.vote_discussion, name='vote_discussion'),
    path('<int:pk>/edit/', views.discussion_edit, name='discussion_edit'),
    path('<int:pk>/delete/', views.discussion_delete, name='discussion_delete'),
]
