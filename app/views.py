from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm, MenuItemForm

def home(request):
    return render(request, "home.html",{})

def restaurant_list(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("restaurant_list")
    else:
        form = RestaurantForm()
    
    restaurants = Restaurant.objects.all()
    return render(request, "restaurant_list.html", {"form":form, "restaurants": restaurants})

def menu_list(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menu_list")
    else:
        form = MenuItemForm()
    
    menu_items = MenuItem.objects.all()
    return render(request, "menu_list.html",{"form" : form, "menu_items" : menu_items})

def combine_form_view(request):
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, prefix = "restaurant")
        menu_form = MenuItemForm(request.POST, prefix = "menu")

        if restaurant_form.is_valid():
            restaurant_form.save()
            return redirect("combined_form")
        
        if menu_form.is_valid():
            menu_form.save()
            return redirect("combined_form")
        
    else:
        restaurant_form = RestaurantForm()
        menu_form = MenuItemForm()

    return render(request, "combined_form.html",{
        "restaurant_form" : restaurant_form,
        "menu_form" : menu_form,
    })