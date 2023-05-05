"""Serializers for the parking place api view"""

from rest_framework import serializers


class ParkingPlaceSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleSerializer()
    status = StatusSerializer()

    class Meta:
        model = ParkingPlace
        # Remember, the following are only fields that users can define themselves
        # through the GUI.
        fields = ["vehicle_type", "status"]

    def create(self, validated_data):
        """Create and return a parking place."""
        return ParkingPlace.objects.create(**validated_data)

    def update(self, instance, data):
        """Update parking place fields and return place."""
        parking_place = super().update(instance, validated_data)

        return parking_place


class VehicleSerializer(serializers.ModelSerializer):

  class Meta:
    model=VehicleType
    fields = ('name')


class StatusSerializer(serializers.ModelSerializer):

  class Meta:
    model=StatusType
    fields = ('name')
