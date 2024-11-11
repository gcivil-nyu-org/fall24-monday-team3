from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartmentPostForm, ApartmentImageForm, CommentForm
from .models import ApartmentImage, ApartmentPost, Rating, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Q
import requests
import os
from dotenv import load_dotenv

load_dotenv(
    "/Users/sreeharshnamani/Downloads/Assignments_NYU/Software/fresh_rentsense/mysite/rentals/map.env"
)

# import PIL


@login_required(login_url="/users/login/")
def apartment_list(request):
    query = request.GET.get("q")
    if query:
        apartments = ApartmentPost.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(address__icontains=query)
        )
    else:
        apartments = ApartmentPost.objects.all()
    context = {"apartments": apartments, "search_query": query}
    return render(request, "rentals/apartment_list.html", context)


@login_required(login_url="/users/login/")
def apartment_detail(request, pk):
    apartment = get_object_or_404(ApartmentPost, pk=pk)
    # Get user's rating for this apartment if it exists
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(post=apartment, user=request.user)
        except Rating.DoesNotExist:
            pass

    comments = apartment.comments.all()  # Load comments for display
    form = CommentForm()  # Empty form for the template
    print(os.getenv("MAP_API"))
    context = {
        "apartment": apartment,
        "user_rating": user_rating,
        "images": apartment.images.all(),
        "comments": comments,
        "form": form,
        "google_maps_api_key": os.getenv("MAP_API"),
    }
    return render(request, "rentals/apartment_detail.html", context)


@login_required(login_url="/users/login/")
def update_apartment_post(request, pk):
    apartment_post = get_object_or_404(ApartmentPost, pk=pk)

    # Check if the user is the owner
    if apartment_post.user != request.user:
        messages.error(request, "You don't have permission to edit this listing.")
        return redirect("apartment_detail", pk=apartment_post.pk)

    if request.method == "POST":
        form = ApartmentPostForm(request.POST, request.FILES, instance=apartment_post)
        if form.is_valid():
            form.save()
            return redirect("apartment_detail", pk=apartment_post.pk)
    else:
        form = ApartmentPostForm(instance=apartment_post)
    return render(
        request,
        "rentals/update_apartment_post.html",
        {"form": form, "post": apartment_post},
    )


@login_required(login_url="/users/login/")
def delete_apartment_post(request, pk):
    apartment_post = get_object_or_404(ApartmentPost, pk=pk)

    # Check if the user is the owner
    if apartment_post.user != request.user:
        messages.error(request, "You don't have permission to delete this listing.")
        return redirect("apartment_detail", pk=apartment_post.pk)

    if request.method == "POST":
        apartment_post.delete()
        messages.success(request, "Apartment listing deleted successfully.")
        return redirect("apartment_list")
    return render(
        request,
        "rentals/delete_apartment_post.html",
        {"apartment_post": apartment_post},
    )


def rate_post(request, post_id):
    if request.method == "POST":
        try:
            post = ApartmentPost.objects.get(id=post_id)
            rating_value = int(request.POST.get("rating"))

            # Update or create rating
            rating, created = Rating.objects.update_or_create(
                post=post, user=request.user, defaults={"value": rating_value}
            )

            # Recalculate average rating
            avg_rating = post.ratings.aggregate(Avg("value"))["value__avg"]
            post.average_rating = round(avg_rating, 2) if avg_rating else 0
            post.save()

            return JsonResponse(
                {
                    "success": True,
                    "average_rating": post.average_rating,
                    "user_rating": rating_value,
                }
            )
        except ApartmentPost.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Post not found"}, status=404
            )
        except ValueError:
            return JsonResponse(
                {"success": False, "error": "Invalid rating value"}, status=400
            )
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


# rentals/views.py
@login_required(login_url="/users/login/")
def clear_rating(request, post_id):
    if request.method == "POST":
        try:
            post = get_object_or_404(ApartmentPost, id=post_id)
            # Delete the user's rating
            Rating.objects.filter(post=post, user=request.user).delete()

            # Recalculate average rating
            avg_rating = post.ratings.aggregate(Avg("value"))["value__avg"]
            post.average_rating = round(avg_rating, 2) if avg_rating else 0
            post.save()

            return JsonResponse(
                {"success": True, "average_rating": post.average_rating}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required(login_url="/users/login/")
def create_apartment_post(request):
    if request.method == "POST":
        post_form = ApartmentPostForm(request.POST)
        image_form = ApartmentImageForm(request.POST, request.FILES)

        if post_form.is_valid() and image_form.is_valid():
            # Create apartment post but don't save to DB yet
            apartment_post = post_form.save(commit=False)
            # Set the user
            apartment_post.user = request.user
            # Now save to DB
            apartment_post.save()
            # Save many-to-many relationships
            post_form.save_m2m()

            apartment_address = apartment_post.address

            images = request.FILES.getlist("image")
            for image in images:
                ApartmentImage.objects.create(apartment=apartment_post, image=image)

            messages.success(request, "Apartment post created successfully!")
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={apartment_address}&key={os.getenv('MAP_API')}"
            response = requests.get(geocode_url).json()
            print(response)
            if response["status"] == "OK":
                location = response["results"][0]["geometry"]["location"]
                apartment_post.latitude = location["lat"]
                apartment_post.longitude = location["lng"]
                apartment_post.save()
            return redirect("apartment_detail", pk=apartment_post.pk)
    else:
        post_form = ApartmentPostForm()
        image_form = ApartmentImageForm()

    context = {"post_form": post_form, "image_form": image_form}
    return render(request, "rentals/create_apartment_post.html", context)


@login_required(login_url="/users/login/")
def search_apartments(request):
    query = request.GET.get("q")
    if query:
        results = ApartmentPost.objects.filter(title__icontains=query)
    else:
        results = ApartmentPost.objects.all()

    return render(
        request, "rentals/search_results.html", {"results": results, "query": query}
    )


@login_required(login_url="/users/login/")
def create_apartment_comment(request, pk):
    post = get_object_or_404(ApartmentPost, pk=pk)
    parent_id = request.POST.get("parent_id")
    parent_comment = None

    # Check if this comment is a reply to another comment
    if parent_id:
        parent_comment = Comment.objects.get(id=parent_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.parent = parent_comment  # Set parent if it's a reply
            comment.save()
            return redirect("apartment_detail", pk=post.pk)

    return redirect("apartment_detail", pk=pk)


@login_required(login_url="/users/login/")
def delete_apartment_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:  # Ensure only the comment author can delete
        comment.delete()
    return redirect("apartment_detail", pk=comment.post.pk)
