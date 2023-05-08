"""
Implement create_parking_lot, which will create a parking lot with 10 spaces to
try out the api.
"""

from parking_place.models import ParkingPlace
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        defaults = {"vehicle_type": "Car", "status": "Empty"}
        for i in range(5):
            ParkingPlace.objects.create(**defaults)
