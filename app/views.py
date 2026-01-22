from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm
from django.views.generic import ListView,CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

def home(request):
    return render(request, "home.html",{})

class RestaurantListView(FormMixin, ListView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurant_list.html"
    success_url = reverse_lazy("restaurant_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return self.get(request, *args, **kwargs)
    
class MenuListView(FormMixin, ListView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menu_list.html"
    success_url = reverse_lazy("menu_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return self.get(request, *args, **kwargs)


class StaffView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "staff_add.html"
    success_url = reverse_lazy("staff_view")

class ShiftView(ListView, CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = "shift.html"
    success_url = reverse_lazy("shift_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context


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