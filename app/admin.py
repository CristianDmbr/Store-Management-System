from django.contrib import admin

from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe

admin.site.register(Restaurant)
admin.site.register(Staff)
admin.site.register(Shift)
admin.site.register(MenuItem)
admin.site.register(Ingredience)
admin.site.register(Recipe)