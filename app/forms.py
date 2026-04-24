from django import forms
from .models import Restaurant, MenuItem, Staff, Shift, Reservation
from django.core.exceptions import ValidationError
from django.utils import timezone

# Semantic contract of clean and clean_<Field name>
# I have seen a def clean_<field> which extracts two different fields from the cleaned_data and it worked.
# Python technically allows it but its best practice to use clean for multiple fields and its a more professional design.

# Difference between extracting name = self.cleaned_data["name_of_reservation"] and restaurant = self.cleaned_data.get("restaurant")
# The name is required and if its missing then it crashes early because something is wrong.
# The restaurant is not as important or might not be temporarily available

# The validation logic of either filtering out or getting the queryset and excluding the current instance.
# I have two different types of validation to check for repetition :
"""# The validation logic of either filtering out or getting the queryset and excluding the current instance.
# I have two different types of validation to check for repetition :
        if name:
            if Restaurant.objects.filter(
                restaurant_name = name
            ).exists():
                raise forms.ValidationError(f"The name {name} is already being used.")
        return name
    
        if name:
            qs = Restaurant.objects.filter(restaurant_name = name)
            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
            if qs.exists():
                raise ValidationError(f"Name : {name} already exists")
        return name"""
# Both versions are safe to use when creating new objects but when it comes to updating the second version is safer.
# In a update  CBV Django uses the instance and knows which row we are currently working on to update so we can exclude from validation
# but with the first version it doesnt know so when we try to update a row it will crash since the row exists and Django doesnt ignore it.
# (Second is more professional and since it handels both CREATE and UPDATE safer)

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = [
            "owner",
            "restaurant_name",
            "date_opened",
            "location",
            "restaurant_cuisine",
            "capacity",
        ]
        widgets = {
            "date_opened": forms.DateInput(attrs={"type": "date"})
        }

    ### Before there was a general def clean() for all of the fields inside one form validation form.
    ### Practice using single field rules def clean_<field>

    def clean_restaurant_name(self):
        name = self.cleaned_data.get("restaurant_name")

        banned_words = [
            "illegal", "banned", "fake", "spam", "scam", "virus",
            "hate", "terror", "bomb", "drugs", "xxx", "nsfw",
            "fraud", "pirate"
        ]

        if name and name.lower() in banned_words:
            raise ValidationError(f"Cannot use the word {name}!")
    
        if name:
            qs = Restaurant.objects.filter(restaurant_name = name)
            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
            if qs.exists():
                raise ValidationError(f"Name : {name} already exists")
        return name
    
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["name_of_reservation","restaurant","number_of_people"]

    def clean(self):

        cleaned_data = super().clean()

        name = cleaned_data.get("name_of_reservation")
        restaurant = cleaned_data.get("restaurant")

        if name and restaurant:
            qs = Reservation.objects.filter(name_of_reservation = name, restaurant = restaurant)
            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
            if qs.exists():
                raise ValidationError(f"{name} already has a reservation at {restaurant}")
        return cleaned_data


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name","surname","date_of_birth","date_employed","position","manager","restaurant","pay_per_hour"]

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
            if qs.exists():
                raise forms.ValidationError(f" {name} {surname} already works here.")
        
        dob = cleaned_data.get("date_of_birth")

        if dob:
            today = timezone.localdate()
            if today < dob:
                raise ValidationError(f"Can't be born before {today}")
        
        return cleaned_data
        

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
            if end_date <= start_date:
                raise forms.ValidationError("End time must be after start time.")
        

class ShiftForEmployeeForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["start_time", "end_time", "status"]

        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["restaurant", "name", "description", "price", "category","calories","availability"]

    def clean(self):
        cleaned_data = super().clean()
        
        name = cleaned_data.get("name")
        restaurant = cleaned_data.get("restaurant")

        if restaurant and name:
            qs = MenuItem.objects.filter(name = name , restaurant = restaurant)
            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f"{name} is already in the {restaurant}'s menu")
        
        
        calories = cleaned_data.get("calories")

    def clean_calories(self):
        cals = self.cleaned_data.get("calories")

        if cals is not None and cals > 1000:
            raise forms.ValidationError(f"Cannot have a item more than 1000kcal, this item has {cals}kcal.")
        
        return cals
    