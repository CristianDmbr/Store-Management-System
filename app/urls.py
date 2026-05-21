from django.urls import path
from .views import (RestaurantListCreateAPI, RestaurantRetrieveUpdateDestroyAPI, HelloWorldView, RestaurantSearchView,
                    ReservationListCreateAPI,ReservationRetrieveUpdateDestroyAPI,
                    StaffListCreateAPI,StaffRetrieveUpdateDestroyAPI,
                    ShiftListCreateAPI,ShiftRetrieveUpdateDestroy,
                    MenuItemRetrieveUpdateDestroyAPI, MenuListCreateAPI)

urlpatterns = [
    # Think of these are not creating two random views, but instead they represent two different levels of the same resource.
    # 90% of the time its only these two types of endpoints you need for your resource (Collection endpoint and Detail endpoint)
    # Collection endpoint (All Restaurants, GET : list all , POST : create)
    path("restaurants/",RestaurantListCreateAPI.as_view(),name="restaurant_create_api"),
    # Detail endpoint (One specific restaurant, GET : retrieve, PUT : update, DELETE: delete)
    path("restaurant/<int:pk>/", RestaurantRetrieveUpdateDestroyAPI.as_view(), name = "restaurant_retrieve_update_destroy_api"),
    path("restaurant/hello", HelloWorldView.as_view(),name = "hello"),
    path("restaurant/search", RestaurantSearchView.as_view(), name = "search_api"),

    path("reservations/",ReservationListCreateAPI.as_view(),name = "reservations_list_create_api"),
    path("reservation/<int:pk>",ReservationRetrieveUpdateDestroyAPI.as_view(), name = "reservation_retrieve_update_destroy_api"),

    path("staff",StaffListCreateAPI.as_view(),name = "staff_list_create_api"),
    path("individual_staff/<str:name>/<str:surname>",StaffRetrieveUpdateDestroyAPI.as_view(), name = "staff_retrieve_update_destroy"),

    path("shifts",ShiftListCreateAPI.as_view(),name = "shift_list_create_api"),
    path("shift/<int:pk>",ShiftRetrieveUpdateDestroy.as_view(),name = "shift_retrieve_update_destroy_api"),

    path("menulist",MenuListCreateAPI.as_view(),name = "menu_list_create_api"),
    path("menuitem/<str:name>/<str:restaurant>",MenuItemRetrieveUpdateDestroyAPI.as_view(),name = "menu_item_retrieve_update_destroy_api"),
]
