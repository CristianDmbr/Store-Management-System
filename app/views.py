from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy

def home(request):
    return render(request, "home.html",{})

class RestaurantListView(ListView, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurant_list.html"
    success_url = reverse_lazy("restaurant_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context
    
#def restaurant_list(request):
#    if request.method == "POST":
#        form = RestaurantForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("restaurant_list")
#        elif not form.is_valid():
#            print(form.errors)
#    else:
#        form = RestaurantForm()
#    
#    restaurants = Restaurant.objects.all()
#   return render(request, "restaurant_list.html", {"form":form, "restaurants": restaurants})

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
        elif not restaurant_form.is_valid():
            print(restaurant_form.errors)

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

def staff_form_view(request):
    if request.method == "POST":
        staff_form = StaffForm(request.POST)

        if staff_form.is_valid():
            staff_form.save()
            return redirect("staff_view")
        else:
            print(staff_form.errors)
    else:
        staff_form = StaffForm()

    
    return render(request, "staff_add.html",{"staff_form" : staff_form})

def shift_view(request):

    if request.method == "POST":
        shift_form = ShiftForm(request.POST)
        
        if shift_form.is_valid():
            shift_form.save()
            return redirect("shift_view")
        else:
            print(shift_form.errors)
    else:
        shift_form = ShiftForm()

    
    return render(request, "shift.html",{"shift_form" : shift_form})

def menu_view(request):

    if request.method == "POST":
        menu_form = MenuItemForm(request.POST)
        if menu_form.is_valid():
            menu_form.save()
            return redirect("menu_add")
        else:
            print(menu_form.erorrs)
    else:
        menu_form = MenuItemForm()
    
    return render(request, "menu_list.html", {"menu_form":menu_form})
