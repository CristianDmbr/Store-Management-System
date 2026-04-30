from django.contrib import admin
from .models import Restaurant, Staff, Shift, MenuItem, Reservation

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "restaurant_name",
        "date_opened",
        "location",
        "restaurant_cuisine",
        "capacity",
        "current_occupancy",
        "remaining_spots",
        "is_full",
    )

@admin.register(Reservation)
class ReservationReservation(admin.ModelAdmin):
    list_display = (
        "name_of_reservation",
        "restaurant",
        "is_active",
        "kids",
        "teens",
        "adults"
    )

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "date_of_birth",
        "date_employed",
        "work_right",
        "position",
        "pay_per_hour",
        "manager",
        "restaurant",
        "age",
    )

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "start_time",
        "end_time",
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "name",
        "description",
        "price",
        "category",
        "availability",
        "date_added",
    )