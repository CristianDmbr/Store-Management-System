from django.contrib import admin
from .models import Restaurant, Staff, Shift, MenuItem, Reservation, Order, OrderItem

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
        "adults",
        "reservation_date_time",
        "phone_number",
        "created_at",
    )

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "date_of_birth",
        "date_time_employed",
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "staff",
        "reservation",
        "date_time_of_order",
        "status",
        "note",
        "table_number",
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "menu_item",
        "quantity",
        "price_sold_at",
    )