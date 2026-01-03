from django.forms import ModelForm
from django import forms
from .models import Restaurant, MenuItem, Staff
from django.core.exceptions import ValidationError

class RestaurantForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        size = cleaned_data.get("size")
        capacity = cleaned_data.get("capacity")

        if size is not None and capacity is not None:
            if capacity < size:
                raise forms.ValidationError(
                    "Capacity must be greater than or equal to size"
                )
    class Meta:
        model = Restaurant
        fields = [
            "owner",
            "restaurant_name",
            "date_opened",
            "location",
            "restaurant_cuisine",
            "size",
            "capacity",
        ]
        widgets = {
            "date_opened": forms.DateInput(attrs={"type": "date"})
        }
    
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant","name","description","price","category","availability"]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant"]

# Create def clean validators for the data in both forms and models