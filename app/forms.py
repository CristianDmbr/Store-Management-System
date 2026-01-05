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
        cleaned_data = super().clean()

        size = cleaned_data.get("size")
        capacity = cleaned_data.get("capacity")

        if size and capacity:
            if size > capacity:
                raise forms.ValidationError(f"Size : {size} cannot be bigger than the restaurant capacity : {capacity}")

        name = cleaned_data.get("restaurant_name")

        banned_words = [
            "illegal",
            "banned",
            "fake",
            "spam",
            "scam",
            "virus",
            "hate",
            "terror",
            "bomb",
            "drugs",
            "xxx",
            "nsfw",
            "fraud",
            "pirate"
        ]

        if name:
            qs = Restaurant.objects.filter( restaurant_name = name)
            if self.instance.pk:
                qs = qs.exclude( pk = self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Name already exists")
    
        if name and name.lower() in [word.lower() for word in banned_words]:
            raise forms.ValidationError(f"Cannot utilise the word {name}")

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","work_right","position","pay_per_hour"]

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant","name","description","price","category","availability"]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant"]

# Create def clean validators for the data in both forms and models