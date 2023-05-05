from django.db import models


class ParkingPlace(models.Model):
    """
    A parking lot is a ParkingPlace table where each row is a parking space.
    Theoretically this is actually a many-many table for VehicleType and
    StatusType, but that's not how it's getting used here.
    """
    vehicle_type = models.ForeignKey("VehicleType", on_delete=models.PROTECT)
    status = models.ForeignKey("StatusType", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.vehicle_type.name}:{self.status.name}"


class VehicleType(models.Model):
    """Possible vehicle types: motorcycle, car, or van."""
    VEHICLE_CHOICES = (
        ("Motorcycle", "Motorcycle"),
        ("Car", "Car"),
        ("Van", "Van"),
    )
    name = models.TextField(max_length=10, blank=False, unique=True, choices=VEHICLE_CHOICES)

    def __str__(self):
        return self.name


class StatusType(models.Model):
    STATUS_CHOICES = (
        ("Free", "Free"), # Not in use.
        ("Adjacent", "Adjacent"), # In use by an adjacent vehicle.
        ("Full", "Full"), # Has something parked in it.
    )
    name = models.TextField(max_length=5, blank=False, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
