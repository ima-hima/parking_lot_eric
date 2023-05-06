"""Django admin customization"""

from django.contrib import admin

from parking_place.models import ParkingPlace


class ParkingPlaceAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["vehicle_type", "status"]
    fieldsets = (
        # First argument is the title of the section.
        (None, {"fields": ("vehicle_type", "status")}),
    )
    readonly_fields = ["id"]

admin.site.register(ParkingPlace)
