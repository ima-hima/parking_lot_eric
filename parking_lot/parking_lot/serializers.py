"""Serializers for the parking place api view"""

# from rest_framework import serializers
# from parking_place.models import ParkingPlace, StatusType, VehicleType


# class ParkingPlaceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ParkingPlace
#         # Remember, the following are only fields that users can define themselves
#         # through the GUI.
#         fields = ["vehicle_type", "status"]

#     def create(self):
#         """Create and return a parking place with default values of an empty car space."""
#         return ParkingPlace.objects.create({"vehicle_type": "Car", "status": "Empty"})

#     def update(self, instance, data):
#         """Update parking place fields and return place."""
#         parking_place = super().update(instance, data)
#         return parking_place


#     # def set_space(self, )



