"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from app import views

# What is a URL (Uniform Resource Locator): the address of a page on a website.

# Why a CBV is in form < views.RestaurantList.as_view() > and why FBV as <views.combine_form_view>?
# FBV : its already a function and Django can call it directly without the <as_view()>
# CBV : is a class and Django cannot call a class directly so it needs the <as_view()>.
#   In urls.py Django expects a callable (a function it can run).
#   So <as_view()> converts a class into a function Django can call.

# The URL patterns which passed keywords doesn't matter.
# The profesional rule for naming a path converter : <Name of template>/<Path Converter>/<Action>
# How path converter works with the example of Restaurant:
# 1. Inside of the restaurant_list.html we display all of the restaurants and next to each row a href ("Where the link should go")
#   where we pass the each individual restaurant pk incase user clicks the edit or delete button.
#   <a href="{% url 'restaurant_edit' restaurant.pk %}">Edit</a>
# 2. When the href is clicked, we mathc the URL name to the actual URL and we pass the restaurant.pk to the view so now 
#   self.object = Restaurant.objects.get(pk = restaurant.pk) so get_object only fetches one row and the form_class is used to display pre filled and 
#   validate that one row.

# URL ROUTER : 

urlpatterns = [
    path('admin/', admin.site.urls),

    # Restaurant
    path("api/my_restaurants/", views.MyRestaurantsAPI.as_view(), name = "my_restaurants_api"), # Collection endpoint
    path("api/detail_restaurant/<int:restaurant_pk>",views.RestaurantDetailAPI.as_view(), name = "detail_restaurant"), # Detail endpoint
    path("api/restaurant_stats/<int:restaurant_pk>",views.RestaurantStatsAPI.as_view(), name = "restaurant_stats"),

    # Staff
    path("api/all_staff",views.MyStaffAPI.as_view(), name = "all_staff"),
    path("api/detail_staff/<int:staff_pk>",views.StaffDetailAPI.as_view(), name = "staff_detail"),

    # Menu Item
    path("api/menu_items_per_restaurants/<int:restaurant_pk>",views.CollectionMenuItempPerRestaurantAPI.as_view(),name = "menu_items_per_restaurant"),
    path("api/menu_items_list", views.CollectionMenuItemAPI.as_view(), name = "menu_item_list"),
    path("api/menu_item_detail/<int:menu_item_pk>", views.DetailMenuItemAPI.as_view(), name = "menu_item_detail"),

    # Shift
    path("api/shift_list",views.CollectionShiftAPI.as_view(),name = "shift_list"),
    path("api/shift_detail/<int:shift_pk>", views.DetailShiftAPI.as_view(), name = "shift_detail"),

    # Reservation
    path("api/reservation_list", views.CollectionReservationAPI.as_view(), name = "reservation_list"),
    path("api/detail_reservation/<int:reservation_pk>", views.DetailReservationAPI.as_view(), name = "reservation_detail"),

    # Order
    path("api/order_list",views.CollectionOrderAPI.as_view(), name = "order_list"),
    path("api/detail_order/<int:order_pk>", views.DetailOrderAPI.as_view(), name = "order_detail"),
    # Update Order status to Complete
    path("api/order_update_to_complete/<int:order_pk>",views.UpdateOrderStatusToComplete.as_view(), name = "update_order_status_to_complete"),
    # Update Order status to Waiting
    path("api/order_update_to_waiting/<int:order_pk>",views.UpdateOrderStatusToWaiting.as_view(), name = "update_order_status_to_waiting"),

    # Order Item
    path("api/order_item", views.CollectionOrderItemAPI.as_view(),name = "order_item_collection"),
    path("api/detail_order_item/<int:order_item_pk>",views.DetailOrderItemAPI.as_view(),name="order_item_detail"),
    # Order items in a Order
    path("api/order_items_per_order/<int:order_pk>",views.OrderItemsOrderBased.as_view(), name = "order_items_for_order"),
    # Decrease Order Item quantity
    path("api/order_menu_item_decrease/<int:order_item_pk>", views.DecreaseOrderItemQuantity.as_view(), name = "decrease_order_menu_item"),

    # Other
    # Gets username of logged in user
    path("api/user_name",views.GetUserLoggedIn.as_view(),name = "user_username"),
    # Login API for users
    path("api/login", views.LoginAPI.as_view(),name = "login_page"),
    # Logout API
    path("api/logout", views.LogoutAPI.as_view(), name = "logout"),
    # Get CSRF token
    path("api/csrf", views.GetCSRFToken.as_view(),name = "csrf_token"),
    # Create a new user using React
    path("api/create_user",views.CreateUserAPI.as_view(), name = "create_user_api"),
    # Dynamic Greetings Message for React
    path("api/time_greetings",views.GetTime.as_view(),name = "time_greetings"),
    # Gather all Supervisors
    path("api/get_supervisors",views.GetAllSupervisors.as_view(),name = "all_supervisors"),
    # Get the restaurant pk / restaurant name for a staff member
    path("api/get_staff_restaurant/", views.GetStaffRestaurant.as_view(), name = "staff_restaurant"),
    # Get the staff Object and pk of a Staff user
    path("api/get_staff_logged_in",views.GetStaffUser.as_view(), name = "get_staff_logged_in"),
    ]