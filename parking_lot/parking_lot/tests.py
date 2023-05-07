from django.test import TestCase
import json

"""Tests for recipe apis"""

from django.test import TestCase
from django.urls import reverse

from parking_place.models import ParkingPlace

from parking_place.views import (
    free_space,
    how_many_spaces_are_vans,
    is_full,
    park,
    set_place_values,
)

# RECIPES_URL = reverse('recipe-list')


def detail_url(space_id):
    """Create and return a parking place detail url."""
    return reverse("parking_place", args=[id])


def create_parking_place(**options):
    """Create and return a sample recipe."""
    defaults = {"vehicle_type": "Car", "status": "Empty"}
    defaults.update(options)
    place = ParkingPlace.objects.create(**defaults)
    return place


def create_parking_lot(num_places, **options):
    """
    Create and return a parking lot, which is a collection of ParkingPlaces.
    Note that what is returned is not the entire parking_space table, but only
    the new spaces created in this fn.
    """
    lot = [create_parking_place(**options) for _ in range(num_places)]
    return lot


class ParkingLotApiTests(TestCase):
    def setUp(self):
        pass

    def test_create_parking_place(self):
        space = create_parking_place()
        self.assertEqual(str(space), "Car:Empty")

    def test_create_parking_lot(self):
        lot = create_parking_lot(5)
        self.assertEqual(
            [str(l) for l in lot],
            ["Car:Empty", "Car:Empty", "Car:Empty", "Car:Empty", "Car:Empty"],
        )

    def test_set_place_values(self):
        lot = create_parking_lot(5)
        set_place_values(lot[1].id, "Motorcycle", "Full")
        place = ParkingPlace.objects.get(id=lot[1].id)
        lot = ParkingPlace.objects.all().order_by("id")
        self.assertEqual(
            [str(l) for l in lot],
            ["Car:Empty", "Motorcycle:Full", "Car:Empty", "Car:Empty", "Car:Empty"],
        )

    def test_is_full_empty_lot(self):
        """Test that an empty lot does appear as full."""
        lot = create_parking_lot(5)
        res = is_full()
        self.assertEqual(res.status_code, 200)
        self.assertFalse(json.loads(res.content)["full"])

    def test_free_space(self):
        lot = create_parking_lot(5)
        set_place_values(lot[1].id, "Motorcycle", "Empty")
        set_place_values(lot[4].id, "Motorcycle", "Full")
        set_place_values(lot[3].id, "Van", "Empty")
        res = free_space()
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"motorcycle": 1, "car": 2, "van": 1}, json.loads(res.content))

    def test_how_many_spaces_are_vans(self):
        lot = create_parking_lot(5)
        set_place_values(lot[1].id, "Car", "Adjacent")
        set_place_values(lot[2].id, "Car", "Full")
        set_place_values(lot[3].id, "Car", "Adjacent")
        set_place_values(lot[4].id, "Van", "Full")
        res = how_many_spaces_are_vans()
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"van-usage": 4}, json.loads(res.content))
        # Now empty the van spot and make sure it goes down by one.
        set_place_values(lot[4].id, "Van", "Empty")
        res = how_many_spaces_are_vans()
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"van-usage": 3}, json.loads(res.content))
        # Now remove adjacent spots and make sure it's 0.
        set_place_values(lot[1].id, "Car", "Empty")
        set_place_values(lot[3].id, "Car", "Empty")
        res = how_many_spaces_are_vans()
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"van-usage": 0}, json.loads(res.content))

    def test_park_car_success(self):
        lot = create_parking_lot(5)
        res = free_space()
        self.assertEqual(res.status_code, 200)
        self.assertEqual({"motorcycle": 0, "car": 5, "van": 0}, json.loads(res.content))
        res = park("car")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(23, json.loads(res.content)["id"])
        lot = ParkingPlace.objects.all().order_by("id")
        self.assertEqual(
            [str(l) for l in lot],
            ["Car:Full", "Car:Empty", "Car:Empty", "Car:Empty", "Car:Empty"],
        )

    def test_park_car_failure(self):
        create_parking_lot(1)
        # self.assertEqual()
        res = park("car")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(22, json.loads(res.content)["id"])
        res = park("car")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(-1, json.loads(res.content)["id"])
