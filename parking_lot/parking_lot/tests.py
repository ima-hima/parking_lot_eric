from django.test import TestCase


"""Tests for recipe apis"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from parking_place.models import ParkingPlace
from parking_lot.serializers import ParkingPlaceSerializer


# RECIPES_URL = reverse('recipe-list')


def detail_url(space_id):
    """Create and return a parking place detail url."""
    return reverse('park', args=[vehicle_type])

def create_parking_place(**options):
    """Create and return a sample recipe."""
    defaults = {"vehicle_type": "Car", "status": "Empty"}
    defaults.update(options)
    place = ParkingPlace.objects.create(**defaults)
    return place


def create_parking_lot(num_places, **options):
    lot = [create_parking_place(options) for _ in range(num_places)]
    return lot


class ParkingLotApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_create_parking_place(self):
        lot = create_parking_lot(5)
        print(lot)
        self.assertEqual(1,0)


    # def test_set_and_to_list(TestCase):
    #     lot = ParkingPlace(5)
    #     for i in range(5):
    #         lot.set_spot(i, "car")
    #     lot.set_spot(3, "motorcycle")
    #     # Check it works
    #     assert lot.to_list() == [
    #         "car:open",
    #         "car:open",
    #         "car:open",
    #         "motorcycle:open",
    #         "car:open",
    #     ]

    # def test_


# class MotorcycleParkingTests(TestCase):
#     """Test API requests that require authentication."""

#     def setUp(self):
#         self.client = APIClient()
#         for i in range(5):
#             create_space()

#     def test_retrieve_recipes(self):
#         """Test retrieving a list of recipes."""
#         create_recipe(user=self.user)
#         create_recipe(user=self.user)

#         res = self.client.get(RECIPES_URL)
#         recipes = Recipe.objects.all().order_by("-id")
#         serializer = RecipeSerializer(recipes, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)


#     def test_park_motorcycle_in_motorcycle_space():
#         lot = ParkingLot(5)
#         lot.set_spot(3, "motorcycle")
#         # Check it works
#         lot.park("motorcycle")
#         assert lot.to_list() == [
#             "car:open",
#             "car:open",
#             "car:open",
#             "motorcycle:full",
#             "car:open",
#         ]
#         # First, force into car spot.
#         lot.park("motorcycle")
#         assert lot.to_list() == [
#             "car:full",
#             "car:open",
#             "car:open",
#             "motorcycle:full",
#             "car:open",
#         ]
#         # Now, force into van spot.
#         lot.unpark(0)
#         assert lot.to_list() == [
#             "car:open",
#             "car:open",
#             "car:open",
#             "motorcycle:full",
#             "car:open",
#         ]
#         lot.set_spot(0, "van")
#         lot.set_spot(1, "van")
#         lot.set_spot(4, "van")
#         assert lot.to_list() == [
#             "van:open",
#             "van:open",
#             "car:open",
#             "motorcycle:full",
#             "van:open",
#         ]
#         lot.park("motorcycle")
#         lot.park("motorcycle")
#         assert lot.to_list() == [
#             "van:full",
#             "van:open",
#             "car:full",
#             "motorcycle:full",
#             "van:open",
#         ]


