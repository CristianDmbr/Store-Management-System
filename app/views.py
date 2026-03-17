from django.shortcuts import render, redirect
from .models import Restaurant, Staff, Shift, MenuItem, Ingredience, Recipe
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

# Understanding GET and POST
# GET : "give me data" and POST : "send/change data"
# GET and POST are part of the HTTP (HyperText Transfer Protocol / how the browser talks to the servers) 
# e.g. When you first open the <restaurant/<int:pk>/edit"> page its a GET request for it to display the template,form and row data.
#      When you click submit then the browser sends a POST request e.g. POST /restaurant/edit]
# def get(self,request, *args, **kwargs): (Shows page)
# def post(self,request), *args, **kwargs): (Handle form submission)
# POST are usually once you submit an, edit, add, delete.
# Why not have Delete or Edit on GET? : Imagive you load a page and it deletes your data or user clicks a link and edits a row.
# Why not display with POST? : Page may break or not load properly.
# SIMPLE RULE:
# 1.GET must be SAFE(no changes on the database)
# 2.POST is for changes
# Inside of the templates you have <form method = "POST"> which indicates when submited browser will send a POST request to the server.

def home(request):
    return render(request, "home.html",{})

class RestaurantList(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"
    # Context object name allows to change the variable name which we use inside of the restaurant_list.html 
    # e.g. : <for restaurant in restaurants>
    context_object_name = "restaurants"

    # get_context_data is a prebuilt Django function which builds the context dictionary sent into the template.
    # Here we just added more info about the page.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "List of all restaurant sorted by date openened."
        return context

    # get_queryset is a prebuilt Django function which determines what data should be retrieved from the database or how to retreive that data.
    # It returns a list of data (Many objects), its used in ListView because it deals with many multiple objects.
    # Main attributes : returns many objects, used in ListView, uses the whole database.
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
    # reverse_lazy doesnt resolve it immediatelly but instead it waits until  URL is needed.
    success_url = reverse_lazy("restaurant_list")


    # UpdateView uses a get_object to get the pk and filter the exact row and then it passes it through the form.
    # GET -> show form (with prefilled data from row), POST -> UPDATE object
class RestaurantUpdate(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "restaurant_update.html"
    success_url = reverse_lazy("restaurant_list")

    #self.kwargs : data coming FROM the URL into the view. Dictionary of values extracted from the URL e.g. with a pk = 5 self.kwarfs = {"pk" : 5}.
    # The reason its called "pk" in the self.kwargs is because we named it like that inside of the <int:pk>.
    # self.kwargs (INPUT to the view) and context (OUTPUT from the view).

    # get_object() returns ONE specific object from the database.
    # Used inside views which deal with a single object: UpdateView, DeleteView, DetailView.
    #(The pk we use inside of the kwargs is from the path converter)
    # Main attributes : returns one object, used in UpdateView, DeleteView, DetailView, it uses pk from the path converter passed to URL.
    # Below you will see how it works by default:
    def get_object(self):
        return Restaurant.objects.get(pk = self.kwargs["pk"])


    # Delete View works almost the same as UpdateView but it retrieves ONE object using a pk and then it deletes it instead of updating it.
    # GET -> show confirmation page (doesnt show prefilled form with data ), POST -> DELETE object
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