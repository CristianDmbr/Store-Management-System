from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

def home(request):
    return render(request, "home.html",{})

class RestaurantList(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"
    context_object_name = "restaurants"

    # get_context_data is a prebuilt Django function which builds the context dictionary sent to the template.
    # Here we just added more info about the page.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "List of all restaurant sorted by date openened."
        return context

    # get_queryset is a prebuilt Django function which determines what data should be retrieved from the database or
    # how to retreive that data.
    def get_queryset(self):
        return Restaurant.objects.order_by("-date_opened")

    # When accessing URL : 1. Creates an empty RestaurantForm. 2. Adds form to the template context. 3. Render the context to the template_name.
    # When submitting the form : 1. Create form with submitted data. 2. Run the validation. 3. If valid we save to DB. 4. Redirect to sucess_url
class RestaurantCreate(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurant_add.html"
    # reverse() converts a URL name into an actual URL. 
    # regular reverse() resolves the url name immediatelly when file loads, at that moment the url might not exist so Django will throw error.
    # reverse_lazy doesnt resolve it immediatelly but instead it waits until URL is needed.
    success_url = reverse_lazy("restaurant_list")


    # UpdateView uses a get_object to get the pk and filter the exact row and then it passes it through the form.
class RestaurantUpdate(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurant_update.html"
    success_url = reverse_lazy("restaurant_list")

class RestaurantDelete(DeleteView):
    model = Restaurant
    template_name = "restaurant_delete.html"
    success_url = reverse_lazy("restaurant_list")

    
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

class StaffList(ListView):
    model = Staff
    template_name = "staff_list.html"

class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = "staff_update.html"
    success_url = reverse_lazy("staff_list")

class StaffDelete(DeleteView):
    model = Staff
    template_name = "staff_delete.html"
    success_url = reverse_lazy("staff_list")

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