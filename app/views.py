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
                    StaffForm,)



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



def staff_list(request):
    all_staff = Staff.objects.all()
    return render(request, 'staff/staff_list.html', {'staff' : all_staff})

def add_restaurant(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    
    return render(request, 'staff/add_staff.html',{'form' : form})