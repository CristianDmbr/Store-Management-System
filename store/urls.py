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
from django.urls import path
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = "home_page"),
    path("menu/", views.MenuListView.as_view(), name = "menu_list"),
    path("shift/", views.ShiftView.as_view(), name = "shift_view"),

    path("restaurants/", views.RestaurantList.as_view(), name = "restaurant_list"),
    path("restaurants_add",views.RestaurantCreate.as_view(), name = "restaurant_create"),
    path("restaurant/<int:pk>/edit",views.RestaurantUpdate.as_view(), name = "restaurant_edit"),
    path("restaurant/<int:pk>/delete",views.RestaurantDelete.as_view(),name = "restaurant_delete"),
    path("reservation/<int:restaurant_id>/create",views.ReservationCreateView.as_view(), name = "create_reservation"),

    path("staff/",views.StaffView.as_view(), name = "staff_view"),  
    path("staff_list/",views.StaffList.as_view(), name = "staff_list"),
    path("staff/<int:pk>/edit",views.StaffUpdateView.as_view(), name = "staff_update"),
    path("staff/<int:pk>/delete", views.StaffDelete.as_view(), name = "staff_delete"),

    path("combined/", views.combine_form_view, name = "combined_form"),
]
