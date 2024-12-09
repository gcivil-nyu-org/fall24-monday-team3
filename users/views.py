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
from alerts.models import Notification
from .models import EmailVerificationToken, PendingEmailChange

User = get_user_model()


@never_cache
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User won't be able to login until email is verified
            user.save()
            
            # Create verification token
            token = EmailVerificationToken.objects.create(user=user)
            
            # Build verification URL
            verify_url = request.build_absolute_uri(
                reverse('verify_email', args=[str(token.token)])
            )
            
            # Send verification email
            send_mail(
                'Verify your RentSense account',
                f'Click the following link to verify your email: {verify_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=f"""
                    <h2>Welcome to RentSense!</h2>
                    <p>Please click the button below to verify your email address:</p>
                    <a href="{verify_url}" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">Verify Email</a>
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p>{verify_url}</p>
                """
            )
            
            # Redirect to verification pending page with email address
            return render(request, 'users/verification_pending.html', {'email': user.email})
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
    try:
        data = json.loads(request.body)
        user = request.user
        email_changed = data.get('email_changed', False)
        new_email = data.get('email')

        if email_changed:
            # Check if email is already taken
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'This email is already in use.'
                })

            # Create pending email change
            pending_change = PendingEmailChange.objects.create(
                user=user,
                new_email=new_email
            )

            # Send verification email
            verify_url = request.build_absolute_uri(
                reverse('verify_email_change', args=[str(pending_change.token)])
            )
            
            send_mail(
                'Verify your new email address',
                f'Click the following link to verify your new email address: {verify_url}',
                settings.DEFAULT_FROM_EMAIL,
                [new_email],
                fail_silently=False,
                html_message=f"""
                    <h2>Verify Your New Email Address</h2>
                    <p>Please click the button below to verify your new email address:</p>
                    <a href="{verify_url}" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">Verify Email</a>
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p>{verify_url}</p>
                """
            )

            # Update other fields except email
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.bio = data.get('bio', user.bio)
            user.save()

            return JsonResponse({
                'success': True,
                'email_verification_required': True
            })
        else:
            # Update all fields including email since it hasn't changed
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.bio = data.get('bio', user.bio)
            user.save()

            return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


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
@require_POST
def send_user_email(request, username):
    try:
        recipient = get_object_or_404(get_user_model(), username=username)
        name = (
            f"{request.user.first_name} {request.user.last_name}"
            if request.user.first_name and request.user.last_name
            else request.user.username
        )
        subject = f"RentSense: Message from {name}"
        message = request.POST.get("message")

        print("\nCreating notification:")
        print(f"Sender: {request.user.username} (ID: {request.user.id})")
        print(f"Recipient: {recipient.username} (ID: {recipient.id})")

        # Create notification ONLY for the recipient
        notification = Notification.objects.create(
            recipient=recipient,  # The person receiving the message
            sender=request.user,  # The person sending the message
            message=f"New message from {name}: {message[:100]}{'...' if len(message) > 100 else ''}",
        )

        # Verify the notification
        saved_notification = Notification.objects.get(id=notification.id)
        print("\nVerified notification in database:")
        print(f"ID: {saved_notification.id}")
        print(
            f"Recipient: {saved_notification.recipient.username} (ID: {saved_notification.recipient.id})"
        )
        print(
            f"Sender: {saved_notification.sender.username} (ID: {saved_notification.sender.id})"
        )

        # HTML email template
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4A90E2;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #ffffff;
                    padding: 20px;
                    border: 1px solid #dddddd;
                    border-radius: 0 0 5px 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>New Message from RentSense</h2>
                </div>
                <div class="content">
                    <p>Hello {recipient.first_name or recipient.username},</p>
                    <p>You have received a message from <strong>{name}</strong>:</p>
                    <p style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">{message}</p>
                    <p>You can reply to this message by visiting their profile on RentSense.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from RentSense. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Send email
        send_mail(
            subject=subject,
            message=f"Hi {recipient.username},\n\nYou have received a message from {name}:\n\n{message}\n\nVisit RentSense to reply.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            html_message=html_message,
        )

        return JsonResponse({"success": True})
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)})


def verify_email(request, token):
    verification = get_object_or_404(EmailVerificationToken, token=token, is_verified=False)
    
    user = verification.user
    user.is_active = True
    user.save()
    
    verification.is_verified = True
    verification.save()
    
    messages.success(request, 'Your email has been verified! You can now log in.', extra_tags='verification')
    return redirect('login')


@login_required
def verify_email_change(request, token):
    pending_change = get_object_or_404(PendingEmailChange, token=token)
    
    # Update user's email
    user = pending_change.user
    user.email = pending_change.new_email
    user.save()
    
    # Delete the pending change
    pending_change.delete()
    
    messages.success(request, 'Your email has been successfully updated!', extra_tags='email_change')
    return redirect('profile')
