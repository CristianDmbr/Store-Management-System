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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = "home_page"),
    path("menu/", views.MenuListView.as_view(), name = "menu_list"),
    path("shift/", views.ShiftView.as_view(), name = "shift_view"),

    path("restaurants/", views.RestaurantList.as_view(), name = "restaurant_list"),
    path("restaurants_add",views.RestaurantCreate.as_view(), name = "restaurant_create"),

    path("staff/",views.StaffView.as_view(), name = "staff_view"),  
    path("staff_list/",views.StaffList.as_view(),name = "staff_list"),
    path("staff/<int:pk>/edit",views.StaffUpdateView.as_view(), name = "staff_update"),
    path("staff/<int:pk>/delete", views.StaffDelete.as_view(), name = "staff_delete"),

    path("combined/", views.combine_form_view, name = "combined_form"),
]
