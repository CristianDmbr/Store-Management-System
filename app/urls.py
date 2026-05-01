from django.urls import path
from .views import RestaurantCreateAPI, RestaurantRetrieveUpdateDestroyAPI

urlpatterns = [
    # Think of these are not creating two random views, but instead they represent two different levels of the same resource.
    # 90% of the time its only these two types of endpoints you need for your resource (Collection endpoint and Detail endpoint)
    # Collection endpoint (All Restaurants, GET : list all , POST : create)
    path("restaurants/",RestaurantCreateAPI.as_view(),name="restaurant_create_api"),
    # Detail endpoint (One specific restaurant, GET : retrieve, PUT : update, DELETE: delete)
    path("restaurant/<int:pk>/", RestaurantRetrieveUpdateDestroyAPI.as_view(), name = "restaurant_retrieve_update_destroy_api"),
]
