from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.chatbot_query, name='chatbot_query'),
    path('', views.chat_interface, name='chat_interface'),
]
