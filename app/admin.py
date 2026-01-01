from django.contrib import admin

from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe

admin.site.register(Staff)
admin.site.register(Shift)
admin.site.register(Ingredience)
admin.site.register(Recipe)

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