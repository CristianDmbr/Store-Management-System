from django import forms
from .models import ( Restaurants, 
                        RestaurantFinance, 
                        Review, 
                        Menu, 
                        Inventory, 
                        CustomerOrder, 
                        Staff, 
                        ShiftManager )
                    
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurants
        fields = ['name','date_opened','restaurant_type','nick_name','capacity']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name','surname','date_of_birth','role']
    
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['restaurant','name','quantity','unit']
