from django.shortcuts import render, redirect
from .models import ( Restaurants, 
                        RestaurantFinance, 
                        Review, 
                        Menu, 
                        Inventory, 
                        CustomerOrder, 
                        Staff, 
                        ShiftManager )

from .forms import (RestaurantForm,
                    StaffForm,
                    InventoryForm)


# Restaurant Related
def restaurant_list(request):
    restaurants = Restaurants.objects.all()
    return render (request, 'restaurant/restaurant_list.html', {'restaurants' : restaurants})

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
        
    return render(request, 'restaurant/add_restaurant.html', {'form' : form})

# Staff Related 
def staff_list(request):
    all_staff = Staff.objects.all()
    return render(request, 'staff/staff_list.html', {'all_staff' : all_staff})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    
    return render(request, 'staff/add_staff.html',{'form' : form})

    ##############
#### Add a shift manager plan which adds shifts and looks if the staff memeber exists and ifts possibel for them ot work at that time
    ##############


# Inventory Related
def inventory_list(request):
    all_inventory = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'all_inventory' : all_inventory})

def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    
    return render(request, 'inventory/add_inventory.html', {'form' : form})