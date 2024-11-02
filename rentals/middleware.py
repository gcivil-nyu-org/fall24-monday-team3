# rentals/middleware.py
# from django.shortcuts import redirect
from django.contrib import messages


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 302 and response.url.startswith("/users/login/"):
            messages.error(request, "Login Required")

        return response
