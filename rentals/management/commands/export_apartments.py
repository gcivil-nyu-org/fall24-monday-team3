# rentals/management/commands/export_apartments.py
import csv
from django.core.management.base import BaseCommand
from rentals.models import ApartmentPost

class Command(BaseCommand):
    help = 'Export apartment data to CSV'

    def handle(self, *args, **kwargs):
        # Extract
        apartments = ApartmentPost.objects.all()

        # Transform & Load
        with open('apartments.csv', 'w', newline='') as csvfile:
            fieldnames = ['title', 'description', 'price', 'address', 'bedrooms', 'square_feet']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for apartment in apartments:
                writer.writerow({
                    'title': apartment.title,
                    'description': apartment.description,
                    'price': apartment.price,
                    'address': apartment.address,
                    'bedrooms': apartment.bedrooms,
                    'square_feet': apartment.square_feet,
                })

        self.stdout.write(self.style.SUCCESS('Data successfully exported to apartments.csv'))

