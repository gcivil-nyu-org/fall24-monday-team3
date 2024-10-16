# rentals/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartmentPostForm, ApartmentImageForm
from .models import ApartmentImage, ApartmentPost
from django.contrib import messages

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
