from django.forms import ValidationError
from django import forms
from .models import Restaurant, MenuItem, Staff, Shift
from django.core.exceptions import ValidationError
from django.utils import timezone


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
            "illegal", "banned", "fake", "spam", "scam", "virus", "hate", "terror", "bomb", "drugs", "xxx", "nsfw", "fraud", "pirate"
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
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant","manager","restaurant"]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"})
        }

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        surname = cleaned_data.get("surname")

        if name and surname:
            qs = Staff.objects.filter(name = name, surname = surname)
            if self.instance.pk:
                qs = qs.exclude( pk = self.instance.pk)
            if qs:
                raise forms.ValidationError(f" {name} {surname} already works here.")
        
        dob = cleaned_data.get("date_of_birth")

        if dob:
            today = timezone.localdate()
            if today < dob:
                raise ValidationError(f"Can't be born before {today}")


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["employee","start_time","end_time"]

        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_time")

        if start_date and end_date:
            if end_date > start_date:
                raise forms.ValidationError("Cant have end before start.")

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant", "name", "description", "price", "category", "availability"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        restaurant = self.cleaned_data.get("restaurant")
        if name and restaurant:
            qs = MenuItem.objects.filter(name=name, restaurant=restaurant)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f"{name} is already on the {restaurant} menu")
        return name

