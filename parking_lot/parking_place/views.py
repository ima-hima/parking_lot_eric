from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from parking_place.models import ParkingPlace


def set_place_values(place_id: int, vehicle_type: str = None, status: str = None):
    """
    Change the vehicle_type and status of the parking place at id==place_id.
    Change only types that are not None.
    """
    place = ParkingPlace.objects.get(id=place_id)
    if vehicle_type:
        place.vehicle_type = vehicle_type
    if status:
        place.status = status
    place.save()


def free_space():
    """Return number of remaining open spaces, motorcycle + car + van."""
    motorcycle_res = ParkingPlace.objects.filter(
        Q(vehicle_type="Motorcycle") & Q(status="Empty")
    ).count()
    car_res = ParkingPlace.objects.filter(
        Q(vehicle_type="Car") & Q(status="Empty")
    ).count()
    van_res = ParkingPlace.objects.filter(
        Q(vehicle_type="Van") & Q(status="Empty")
    ).count()
    return JsonResponse({"motorcycle": motorcycle_res, "car": car_res, "van": van_res})


def how_many_spaces_are_vans() -> int:
    """Return the total number of spaces used by vans."""
    van_spaces = ParkingPlace.objects.filter(
        Q(vehicle_type="Van") & Q(status="Full")
    ).count()
    adjacent_spaces = ParkingPlace.objects.filter(status="Adjacent").count()
    total = van_spaces + adjacent_spaces // 2 * 3
    return JsonResponse({"van-usage": total})


def park(vehicle_type: str) -> int:
    """
    Attempt to park a vehicle (motorcycle, car, or van). If succesful, return
    space number. Otherwise, return -1.
    """

    # Move a space from an "open" set to a "full" set. For each incoming
    # vehicle type check for open spaces in increasing order of size.

    # Note that, for any given vehicle to be parked, a space is chosen at random,
    # meaning that over time vans may become more difficult to park. I believe
    # that Python sets are lrus, but choosing from an ordered list might be more
    # efficient.
    if json.loads(is_full().content):
        return JsonResponse({"id": -1})

    space_dict = json.loads(free_space().content)

    if vehicle_type.lower() == "motorcycle":
        # Check first for motorcycle spaces, then cars spaces, then van spaces.
        if space_dict["motorcycle"]:
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Motorcycle") & Q(status="Empty")
            ).id
        elif space_dict["car"]:
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Car") & Q(status="Empty")
            ).id
        else:
            # There must be a van space available.
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            ).id
        set_place_values(space_number, status="Full")
        return space_number
    elif vehicle_type.lower() == "car":
        # Check first for car spaces, then for van spaces.
        if space_dict["car"]:
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Car") & Q(status="Empty")
            ).id
        else:
            # There must be a van space available.
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            ).id
        set_place_values(space_number, status="Full")
        return space_number
    elif vehicle_type.lower() == "van":
        # It's a van. Look for van spaces, if not available try for three
        # car spaces.
        if space_dict["van"]:
            space_number = ParkingPlace.objects.filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            ).id
            set_place_values(space_number, status="Full")
        elif space_dict["car"] > 2:
            space_number = ParkingPlace.objects.raw(
                "SELECT id FROM parking_place p"
                "              JOIN parking_place q"
                "              JOIN park_place r"
                'WHERE p.vehicle_type="Car"'
                '  AND p.status="Empty"'
                '  AND q.vehicle_type="Car"'
                '  AND q.status="Empty"'
                '  AND r.vehicle_type="Car"'
                '  AND r.status="Empty"'
                "  AND q.id = p.id - 1"
                "  AND r.id = p.id + 1"
            )
            if space_number:
                set_place_values(space_number, status="Full")
                set_place_values(space_number - 1, status="Adjacent")
                set_place_values(space_number + 1, status="Adjacent")
        else:
            # There were no van spaces and not enough car spaces.
            return -1
    else:
        # The input is bad
        return JsonResponse({"id": -1})
    return space_number


def unpark(space_number: int) -> bool:
    """
    Remove the vehicle from a space. Return True if the space was taken, False
    otherwise. Only a boolean is returned because the type of vehicle in a
    given space has not been tracked.
    """
    pass


def is_full() -> bool:
    """
    Return True if lot is full, False otherwise. Note this does not mean there
    is space for a van or a car, as for instance, only a single motorcycle
    space might be available.
    """
    res = ParkingPlace.objects.filter(status__exact="Empty").count()
    return JsonResponse({"full": res == 0})


# class ParkingPlaceViewSet(viewsets.ModelViewSet):
#     """View for managing parking apis"""
#     serializer_class = serializers.ParkingPlaceSerializer
#     queryset = ParkingPlace.objects.all()

#     def get_queryset(self):
#         """Retrieve parking lot (all parking places in DB)."""
#         return self.queryset.order_by('id')

#     def update(self, **updates):
