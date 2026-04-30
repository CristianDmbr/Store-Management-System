from django.urls import path
from .views import RestaurantCreateAPI

urlpatterns = [
    path("restaurants/",RestaurantCreateAPI.as_view(),name="restaurant_create_api"),
]
