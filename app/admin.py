from django.contrib import admin
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "start_time",
        "end_time",
    )

@admin.register(Ingredience)
class IngredienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "quantity_in_stock",
        "units",
    )

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "menu_item",
        "ingredience",
        "quantity",
        "unit"
    )

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "restaurant_name",
        "date_opened",
        "location",
        "restaurant_cuisine",
        "size",
        "capacity",
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
    )