from django.db import models


class ParkingSpace(models.Model):
    vehicle_type = models.ForeignKey("VehicleType"), on_delete=models.PROTECT)
    is_full = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_type.name}:{self.is_full}"


class VehicleType(models.Model):
    CHOICES = (
        ("Motorcycle", "Motorcycle"),
        ("Car", "Car"),
        ("Van", "Van"),
    )
    name = models.TextField(max_length=10, blank=False, unique=True, choices=CHOICES)

    def __str__(self):
        return self.name
