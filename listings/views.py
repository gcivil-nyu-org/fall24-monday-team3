from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, get_object_or_404, redirect
from .models import Rental
from django.http import HttpResponse

# Update view
def update_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == "POST":
        rental.title = request.POST['title']
        rental.description = request.POST['description']
        rental.price = request.POST['price']
        rental.location = request.POST['location']
        rental.apartment_type = request.POST['apartment_type']
        rental.sqft = request.POST['sqft']
        rental.amenities = request.POST['amenities']
        rental.save()
        return redirect('rental_detail', rental_id=rental.id)
    return render(request, 'listings/update_rental.html', {'rental': rental})

# Delete view
def delete_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == "POST":
        rental.delete()
        return redirect('rental_list')
    return render(request, 'listings/delete_rental.html', {'rental': rental})

def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    return render(request, 'listings/rental_detail.html', {'rental': rental})

def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, 'listings/rental_list.html', {'rentals': rentals})
