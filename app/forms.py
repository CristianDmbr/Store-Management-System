from django.forms import ModelForm
from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["owner","restaurant_name","date_opened","location","restaurant_cuisine","size","capacity"]
        widgets = {
            "date_opened": forms.DateInput(attrs={"type": "date"})}