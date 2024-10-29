from django.shortcuts import render, get_object_or_404, redirect
from .models import Rental
from .forms import RentalForm


# List view
def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, "listings/rental_list.html", {"rentals": rentals})


# Create view
def create_rental(request):
    if request.method == "POST":
        form = RentalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("rental_list")
    else:
        form = RentalForm()
    return render(request, "listings/create_rental.html", {"form": form})


# Detail view
def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    return render(request, "listings/rental_detail.html", {"rental": rental})


# Update view
def update_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == "POST":
        form = RentalForm(request.POST, request.FILES, instance=rental)
        if form.is_valid():
            form.save()
            return redirect("rental_detail", rental_id=rental.id)
    else:
        form = RentalForm(instance=rental)
    return render(request, "listings/update_rental.html", {"form": form})


# Delete view
def delete_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if request.method == "POST":
        rental.delete()
        return redirect("rental_list")
    return render(request, "listings/delete_rental.html", {"rental": rental})
