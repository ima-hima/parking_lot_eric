import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.db import connection

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


def free_space(request):
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


def how_many_spaces_are_vans(request):
    """Return the total number of spaces used by vans."""
    van_spaces = ParkingPlace.objects.filter(
        Q(vehicle_type="Van") & Q(status="Full")
    ).count()
    adjacent_spaces = ParkingPlace.objects.filter(status="Adjacent").count()
    total = van_spaces + adjacent_spaces // 2 * 3
    return JsonResponse({"van-usage": total})


def park(request, vehicle_type: str) -> JsonResponse:
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
    if json.loads(is_full(request).content)["full"]:
        return JsonResponse({"id": -1})

    space_dict = json.loads(free_space(request).content)
    if vehicle_type.lower() == "motorcycle":
        # Check first for motorcycle spaces, then cars spaces, then van spaces.
        if space_dict["motorcycle"]:
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Motorcycle") & Q(status="Empty")
            )[0]["id"]
        elif space_dict["car"]:
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Car") & Q(status="Empty")
            )[0]["id"]
        else:
            # There must be a van space available.
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            )[0]["id"]
        set_place_values(space_number, status="Full")
        return JsonResponse({"id": space_number})
    elif vehicle_type.lower() == "car":
        # Check first for car spaces, then for van spaces.
        if space_dict["car"]:
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Car") & Q(status="Empty")
            )[0]["id"]
        else:
            # There must be a van space available.
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            )[0]["id"]
        set_place_values(space_number, status="Full")
        return JsonResponse({"id": space_number})
    elif vehicle_type.lower() == "van":
        # It's a van. Look for van spaces, if not available try for three
        # car spaces.
        if space_dict["van"]:
            space_number = ParkingPlace.objects.values("id").filter(
                Q(vehicle_type="Van") & Q(status="Empty")
            )[0]["id"]
            set_place_values(space_number, status="Full")
            return JsonResponse({"id": space_number})
        elif space_dict["car"] > 2:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT p.id FROM parking_place_parkingplace p
                                  JOIN parking_place_parkingplace q ON p.id - 1 = q.id
                                  JOIN parking_place_parkingplace r ON p.id + 1 = r.id
                    WHERE p.vehicle_type = 'Car'
                      AND p.status = 'Empty'
                      AND q.vehicle_type = 'Car'
                      AND q.status='Empty'
                      AND r.vehicle_type='Car'
                      AND r.status='Empty'
                    LIMIT 1;""")
                space_number = cursor.fetchone()[0]
                set_place_values(space_number, status="Van")
                set_place_values(space_number - 1, status="Adjacent")
                set_place_values(space_number + 1, status="Adjacent")
                return JsonResponse({"id": space_number})
        else:
            # There were no van spaces and not enough car spaces.
            return JsonResponse({"id": -1})
    else:
        # The input is bad
        return JsonResponse({"id": -1})
    return JsonResponse({"id": space_number})


def unpark(request, space_number: int):
    """
    Remove the vehicle from a space. Return True if the space was taken, False
    otherwise. Only a boolean is returned because the type of vehicle in a
    given space has not been tracked.
    """
    space_vals = ParkingPlace.objects.values("status", "vehicle_type").get(id=space_number)
    if space_vals["vehicle_type"] == "Motorcycle" or space_vals["vehicle_type"] == "Van":
        # We don't have to worry about the special case of a van taking three
        # spaces.
        set_place_values(space_number, status="Empty")
        return JsonResponse({"success": True})

    if space_vals["status"] == "Van":
        # We need to worry about adjacent spaces.
        set_place_values(space_number, status="Empty")
        set_place_values(space_number - 1, status="Empty")
        set_place_values(space_number + 1, status="Empty")
        return JsonResponse({"success": True})

    if space_vals["status"] != "Adjacent":
        # We know it's not adjacent and it's not a van or motorcycle space.
        # We can just set it to Empty.
        set_place_values(space_number, status="Empty")
        return JsonResponse({"success": True})

    # If we got this far something went wrong.
    return JsonResponse({"success": False})



def is_full(request):
    """
    Return True if lot is full, False otherwise. Note this does not mean there
    is space for a van or a car, as for instance, only a single motorcycle
    space might be available.
    """
    res = ParkingPlace.objects.filter(status__exact="Empty").count()
    return JsonResponse({"full": res == 0})


