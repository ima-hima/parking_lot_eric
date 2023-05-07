from django.contrib import admin
from django.urls import path, include

from parking_place import views

app_name = "parking_lot"

urlpatterns = [
    path("park/<str:type>/", views.park),
    path("vans-usage", views.how_many_spaces_are_vans),
    path("free", views.free_space),
    path("is-full", views.is_full),
]
