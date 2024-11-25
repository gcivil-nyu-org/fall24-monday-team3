from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rentals.models import Favorite as RentalFavorite
from roommates.models import Favorite as RoommateFavorite
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_control

@never_cache
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_view(request):
    return render(request, "users/register.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_view(request):
    return render(request, "users/home.html")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_view(request):
    rental_favorites = RentalFavorite.objects.filter(user=request.user).select_related(
        "post"
    )
    roommate_favorites = RoommateFavorite.objects.filter(
        user=request.user
    ).select_related("post")

    context = {
        "rental_favorites": rental_favorites,
        "roommate_favorites": roommate_favorites,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_http_methods(["POST"])
@never_cache
def edit_profile(request):
    try:
        data = json.loads(request.body)
        user = request.user
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.email = data.get("email")
        user.bio = data.get("bio")
        user.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
@never_cache
def delete_favorite(request, type, favorite_id):
    try:
        if type == "rental":
            favorite = RentalFavorite.objects.get(id=favorite_id, user=request.user)
        else:
            favorite = RoommateFavorite.objects.get(id=favorite_id, user=request.user)

        favorite.delete()
        return JsonResponse({"success": True})
    except (RentalFavorite.DoesNotExist, RoommateFavorite.DoesNotExist):
        return JsonResponse({"success": False}, status=404)
