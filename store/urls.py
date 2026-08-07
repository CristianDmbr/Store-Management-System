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

    path("", LoginView.as_view(template_name = "login.html"),name = "login_page"),
    path("register",views.register,name = "register_page"),
    path("dashboard_router/", views.dashboard_router, name = "dashboard_router"),
    path("logout",LogoutView.as_view(next_page = "login_page"),name = "logout"),

    # Manager Role
    path("owner/home_dashboard",views.owner_dashboard_home, name = "owner_dashboard_home"),

    # Supervisor
    path("supervisor/home_dashboard", views.supervisor_dashboard_home, name ="supervisor_dashboard_home"),

    # Staff Role
    path("staff/home_dashboard",views.staff_dashboard_home, name = "staff_dashboard_home"),

    # Restaurants
    path("restaurant_lists",views.display_all_restaurants, name = "display_all_owned_restaurants"),
    path("add_new_restaurant",views.add_new_restaurant, name = "add_new_restaurant"),
    path("delete_restaurant/<int:restaurant_pk>/",views.delete_restaurant, name = "delete_restaurant"),
    path("update_restaurant/<int:restaurant_pk>/", views.update_restaurant, name = "update_restaurant"),
    path("view_restaurant/<int:restaurant_pk>",views.restaurant_full_info, name = "restaurant_info"),

    # Staff Model
    path("general_staff_list",views.display_all_staff, name = "display_all_staff"),
    path("delete_staff/<int:staff_pk>",views.delete_staff, name = "delete_staff"),
    path("add_staff>",views.add_staff, name = "add_staff"),
]
 