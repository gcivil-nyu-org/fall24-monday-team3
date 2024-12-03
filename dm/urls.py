# urls.py
from django.urls import path
from . import views

app_name = "dm"  # Ensure this matches the namespace you're using

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("conversation/<str:username>/", views.conversation, name="conversation"),
    path("send_message/", views.send_message, name="send_message"),
]
