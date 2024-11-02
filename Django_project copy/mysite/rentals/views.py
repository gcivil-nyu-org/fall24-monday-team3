from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartmentPostForm, ApartmentImageForm
from .models import ApartmentImage, ApartmentPost, Rating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Q

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

    context = {
        "apartment": apartment,
        "user_rating": user_rating,
        "images": apartment.images.all(),
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

            images = request.FILES.getlist("image")
            for image in images:
                ApartmentImage.objects.create(apartment=apartment_post, image=image)

            messages.success(request, "Apartment post created successfully!")
            return redirect("apartment_detail", pk=apartment_post.pk)
    else:
        post_form = ApartmentPostForm()
        image_form = ApartmentImageForm()

    context = {"post_form": post_form, "image_form": image_form}
    return render(request, "rentals/create_apartment_post.html", context)
