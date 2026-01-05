from django.forms import ModelForm, ValidationError
from django import forms
from .models import Restaurant, MenuItem, Staff
from django.core.exceptions import ValidationError

class RestaurantForm(forms.ModelForm):

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

    def clean(self):
            clean_date = super().clean()
            cleaned_size = clean_date.get("size")
            cleaned_capacity = clean_date.get("capacity")

            if cleaned_size and cleaned_capacity:
                if cleaned_size > cleaned_capacity:
                    raise forms.ValidationError("Can't have a size bigger than the capacity :(")

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant","name","description","price","category","availability"]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant"]

# Create def clean validators for the data in both forms and models