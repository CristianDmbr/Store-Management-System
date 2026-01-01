from django.forms import ModelForm
from django import forms
from .models import Restaurant, MenuItem, Staff

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["owner","restaurant_name","date_opened","location","restaurant_cuisine","size","capacity"]
        widgets = {
            "date_opened": forms.DateInput(attrs={"type": "date"})}
    
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant","name","description","price","category","availability"]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant"]