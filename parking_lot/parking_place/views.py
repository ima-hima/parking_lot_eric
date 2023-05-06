from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from models import ParkingPlace
from recipe import serializers


class ParkingPlaceViewSet(viewsets.ModelViewSet):
    """View for managing parking apis"""
    serializer_class = serializers.ParkingPlaceSerializer
    queryset = ParkingPlace.objects.all()

    def get_queryset(self):
        """Retrieve parking lot (all parking places)."""
        return self.queryset.order_by('id')
