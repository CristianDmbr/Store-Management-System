from django.contrib import admin
from app.models import ( Restaurants, 
                        RestaurantFinance, 
                        Review, 
                        Menu, 
                        Inventory, 
                        CostumerOrder, 
                        Staff, 
                        ShiftManager )

admin.site.register(Restaurants)
admin.site.register(RestaurantFinance)
admin.site.register(Review)
admin.site.register(Menu)
admin.site.register(Inventory)
admin.site.register(CostumerOrder)
admin.site.register(Staff)
admin.site.register(ShiftManager)