from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
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
from rentals.models import ApartmentPost
from roommates.models import RoommatePost
from discussions.models import Discussion
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerificationToken, PendingEmailChange

User = get_user_model()


@never_cache
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check if email already exists
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                form.add_error("email", "This email address is already in use.")
                return render(request, "users/signup.html", {"form": form})

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Create verification token
            token = EmailVerificationToken.objects.create(user=user)

            # Build verification URL
            verify_url = request.build_absolute_uri(
                reverse("verify_email", args=[str(token.token)])
            )

            # Send verification email
            send_mail(
                "Verify your RentSense account",
                f"Click the following link to verify your email: {verify_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=f"""
                    <h2>Welcome to RentSense!</h2>
                    <p>Please click the button below to verify your email address:</p>
                    <a href="{verify_url}" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">Verify Email</a>
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p>{verify_url}</p>
                """,
            )

            return render(
                request, "users/verification_pending.html", {"email": user.email}
            )
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
                return redirect("home")
        form.add_error(None, "Invalid username or password")
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
    user_rental_posts = ApartmentPost.objects.filter(user=request.user).order_by("-id")
    user_roommate_posts = RoommatePost.objects.filter(user=request.user).order_by("-id")
    user_discussion_posts = Discussion.objects.filter(author=request.user).order_by(
        "-created_at"
    )

    context = {
        "rental_favorites": rental_favorites,
        "roommate_favorites": roommate_favorites,
        "user_rental_posts": user_rental_posts,
        "user_roommate_posts": user_roommate_posts,
        "user_discussion_posts": user_discussion_posts,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_http_methods(["POST"])
def edit_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            email_changed = data.get("email_changed", False)
            new_email = data.get("email")

            # Check for duplicate email
            if email_changed and new_email:
                if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                    return JsonResponse(
                        {"success": False, "error": "This email is already in use."}
                    )

            # Update user fields
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.bio = data.get("bio", user.bio)

            if email_changed and new_email:
                # Create pending email change
                PendingEmailChange.objects.filter(user=user).delete()
                pending_change = PendingEmailChange.objects.create(
                    user=user, new_email=new_email
                )

                # Send verification email
                verification_url = request.build_absolute_uri(
                    reverse(
                        "verify_email_change", kwargs={"token": pending_change.token}
                    )
                )
                send_mail(
                    "Verify your new email address",
                    f"Please click the following link to verify your new email address: {verification_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [new_email],
                    fail_silently=False,
                )
                return JsonResponse(
                    {
                        "success": True,
                        "email_verification_required": True,
                        "message": "A verification email has been sent. The email change will be applied once verified.",
                    }
                )
            else:
                user.email = data.get("email", user.email)

            user.save()
            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})

    return render(request, "users/edit_profile.html")


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


@login_required(login_url="/users/login/")
def public_profile(request, username):
    profile_user = get_object_or_404(get_user_model(), username=username)

    context = {
        "profile_user": profile_user,
        "user_rental_posts": ApartmentPost.objects.filter(user=profile_user).order_by(
            "-id"
        ),
        "user_roommate_posts": RoommatePost.objects.filter(user=profile_user).order_by(
            "-id"
        ),
        "user_discussion_posts": Discussion.objects.filter(
            author=profile_user
        ).order_by("-created_at"),
    }

    return render(request, "users/public_profile.html", context)


@login_required(login_url="/users/login/")
def discussion_create(request):
    if request.method == "POST":
        form = Discussion(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            return redirect(
                reverse("discussions:discussion_detail", args=[discussion.pk])
            )
    else:
        form = Discussion()
    return render(request, "discussions/discussion_form.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def send_user_email(request, username):
    if not request.content_type == "application/json":
        return JsonResponse(
            {"success": False, "error": "Content-Type must be application/json"},
            status=400,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "User not found"},
            status=404,
            content_type="application/json",
        )

    subject = data.get("subject")
    message = data.get("message")

    if not subject or not message:
        return JsonResponse(
            {"success": False, "error": "Missing subject or message"},
            status=400,
            content_type="application/json",
        )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
        )
        return JsonResponse({"success": True}, content_type="application/json")
    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
            content_type="application/json",
        )


def verify_email(request, token):
    verification = get_object_or_404(
        EmailVerificationToken, token=token, is_verified=False
    )

    user = verification.user
    user.is_active = True
    user.save()

    verification.is_verified = True
    verification.save()

    messages.success(
        request,
        "Your email has been verified! You can now log in.",
        extra_tags="verification",
    )
    return redirect("login")


@login_required
def verify_email_change(request, token):
    pending_change = get_object_or_404(PendingEmailChange, token=token)

    # Update user's email
    user = pending_change.user
    user.email = pending_change.new_email
    user.save()

    # Delete the pending change
    pending_change.delete()

    messages.success(
        request, "Your email has been successfully updated!", extra_tags="email_change"
    )
    return redirect("profile")  # This now matches the URL name
