from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm

def restaurant_list(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("restaurant_list")
    else:
        form = RestaurantForm
    
    restaurants = Restaurant.objects.all()
    return render(request, "restaurant_list.html", {"form":form, "restaurants":
    restaurants})

