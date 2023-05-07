from django.contrib import admin
from django.urls import path, include

from parking_place import views

app_name = "parking_lot"

urlpatterns = [
    path("park/<str:type>/", views.park),
    # path("admin/", admin.site.urls),
    # path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    # path(
    #     "api/docs/",
    #     SpectacularSwaggerView.as_view(url_name="api-schema"),
    #     name="api-docs",
    # ),
    # path("set-spot/", views.SetSpotView.as_view(), name="set_spot")
    path("vans-usage", views.how_many_spaces_are_vans),
    path("free", views.free_space),
]
