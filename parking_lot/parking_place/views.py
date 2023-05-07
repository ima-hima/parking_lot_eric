from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from parking_place.models import ParkingPlace



def free_space(self):
    """Return number of remaining open spaces, motorcycle + car + van."""
    free = ParkingPlace.objects.filter(status="Empty").count()

    return JsonResponse({"free-spaces": free})


def how_many_spaces_are_vans(self) -> int:
    """Return the total number of spaces used by vans."""
    # With "Q()" and "&"
    van_spaces = ParkingPlace.objects.filter(
                                 Q(vehicle_type="Van") &
                                 Q(status="Full")).count()
    adjacent_spaces = ParkingPlace.objects.filter(status="Adjacent").count()
    total = van_spaces + adjacent_spaces // 2 * 3
    return JsonResponse({"van-usage": total})


def park(self, type: str) -> int:
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
    pass



def unpark(self, space_number: int) -> bool:
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


