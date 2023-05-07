from django.db import models


class ParkingPlace(models.Model):
    """
    A parking lot is a ParkingPlace table where each row is a parking space.
    Theoretically this is actually a many-many table for VehicleType and
    StatusType, but that's not how it's getting used here.
    """

    """
    Status of a spot: is it in use or empty. Note that there are two other values.
    Adjacent means it's a spot adjecent to a van parked in a car place. Van
    denotes a car spot with a van in it. We need both of these in order to
    correctly unpark vans. Without these values vans parked next to cars or
    vans in car spots next to each other would be difficult to detect.
    """
    STATUS_CHOICES = (
        ("Empty", "Empty"),  # Parking place is not in use.
        ("Adjacent", "Adjacent"),  # In use by an adjacent vehicle.
        ("Full", "Full"),  # Has something parked in it.
        ("Van", "Van"), # Specifically to mark a car with a van in it.
    )
    VEHICLE_CHOICES = (
        ("Motorcycle", "Motorcycle"),
        ("Car", "Car"),
        ("Van", "Van"),
    )
    vehicle_type = models.TextField(max_length=10, blank=False, choices=VEHICLE_CHOICES)
    status = models.TextField(max_length=8, blank=False, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.vehicle_type}:{self.status}"
