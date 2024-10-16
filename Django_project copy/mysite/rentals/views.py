# rentals/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartmentPostForm, ApartmentImageForm
from .models import ApartmentImage, ApartmentPost, Rating
from django.contrib import messages
import PIL
from django.http import JsonResponse
from django.db.models import Avg

def apartment_list(request):
    apartments = ApartmentPost.objects.all()
    context = {
        'apartments': apartments
    }
    return render(request, 'rentals/apartment_list.html', context)

def apartment_detail(request, pk):
    apartment = get_object_or_404(ApartmentPost, pk=pk)
    images = apartment.images.all()
    context = {
        'apartment': apartment,
        'image': images
    }
    return render(request, 'rentals/apartment_detail.html', context)

def create_apartment_post(request):
    if request.method == 'POST':
        post_form = ApartmentPostForm(request.POST)
        image_form = ApartmentImageForm(request.POST, request.FILES)

        if post_form.is_valid() and image_form.is_valid():
            apartment_post = post_form.save()
            images = request.FILES.getlist('image')

            for image in images:
                ApartmentImage.objects.create(apartment=apartment_post, image=image)

            messages.success(request, "Apartment post created successfully!")
            return redirect('apartment_detail', pk=apartment_post.pk)
    else:
        post_form = ApartmentPostForm()
        image_form = ApartmentImageForm()

    context = {
        'post_form': post_form,
        'image_form': image_form
    }
    return render(request, 'rentals/create_apartment_post.html', context)

def rate_post(request, post_id):
    if request.method == 'POST':
        try:
            post = ApartmentPost.objects.get(id=post_id)
            rating_value = int(request.POST.get('rating'))
            
            Rating.objects.create(post=post, value=rating_value)
            
            # Recalculate average rating
            avg_rating = post.ratings.aggregate(Avg('value'))['value__avg']
            post.average_rating = round(avg_rating, 2) if avg_rating else 0
            post.save()
            
            return JsonResponse({'success': True, 'average_rating': post.average_rating})
        except ApartmentPost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid rating value'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
