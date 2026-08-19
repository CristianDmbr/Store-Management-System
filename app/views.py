from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Staff, Shift, MenuItem, Reservation, Order,OrderItem
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm, ReservationForm,ShiftForEmployeeForm, UserRoleCreationForm, StaffFormSupervisor, OrderForm, OrderItemForm
from .serialisers import RestaurantSerialiser, ReservationSerialiser, StaffSerialiser, ShiftSerialiser, MenuItemSerialiser
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required 

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseForbidden

from rest_framework import generics,status
from rest_framework.response import Response
# Create custom API views
from rest_framework.views import APIView
from datetime import date, timedelta, datetime
from django.utils import timezone



# Client is anything that sends request to a server e.g. Browser, Mobile App

# ORM (Object Relational Mapper) : communicating and updating the DB throught python code.

# DRF page:
# Not a HTML and used for debugging, testing and debugging API so not real website URL, not meant for users and you cannot design navigation
   
# DRF is an extension of Django that lets you build APIs instead of HTML pages.
# Django (Uses FBV or CBV) [request -> View -> Template -> HTML]
# DRF (Functions are called serialisers either Manual API or Generic Views) [request -> View -> Serialisation -> JSON]
# A APIView (manual API) lets you control everything similar to a FBV.
# A Generic View less code, prebuilt, faster development and similar to a CBV
# What is an endpoint : a URL that the backend exposes for interaction whether thats for CBV or API, and a URL that your backend responds to
# What is a resource : data entity in your system (model) e.g. Restaurant, Staff, Reservation. 
# Django CBV: Each URL is a page for a human where each one offers a different purpose or experience.
# But for API each URL is a resource, meaning /api/restaurants/ is not show me a page but its, this is the collection of Restaurant data.
# HTTP GET,POST,PUT,DELETE 
# Resource endpoint : URL representing a resource.
# CBV (HTML) is designed for humans (Browser UI) but API (DRF) are designed for systems (frontend,apps etc... or you can still open it on browser for testing)
# DRF design thinkgs of what data do I expose? not what page do I need?
# CBV thinking : I need a page to edit a restaurant
# DRF thinking : This page exposes restaurant data (ALSO one resource endpoint can allow the Frontend to do all GET,POST,PUT,DELETE all using the same URL)
# But DRF still allows for API methods which do one thing, why ? Because if endpoint is simple then we can combine, if its complex then we can split and work on them seperately

# DRF Pipeline : First query all of the database with model objects we need, serilatiser converts it into a python list of dictionaries (NOT JASON YET),
# its the Response(serialisation.data) that converts the python doc into a JSON file. (We only see the Response be used in a cutome DRF view, in a generic ints used in the back)

# CBV pipeline : First user makes a HTTP request of GET, the URL routes the request to the CBV, The CBV queries the database, the get_queryset() gets the database data,
# then the get_context_data puts that data into a context dictionary as a object_list or custom say context_object_name = ""
# context is the actual dictionary that gets sent to tempalte but get_context_data is what muilds/modifies this template

# Difference between .filter() and .get()
# .filter() : returns a queryset (collection, even if its only one object)
# .get() : returns only one single model object
 
# Path param and query param
# Both are part of HTTP and not just DRF so you can use them in any views not just DRF
# Path param /api/restaurant/1/ where the 1 is a param in the route restaurant/<int:pk>
# Query param /api/restaurant/search where its not mentioned in the route
# In Django say http://127.0.0.1:8000/api/restaurant/search?name=pizza Django only looks until api/restaurant/ and the rest is extra data
# which can be extracted from request.query_param.get() and it can be used to get more than one object
# /restaurant/5/ give me this exact object, /search?name=pizza give me objects with this condition
#     Path params → easy ({% url ... pk %})
# But how do users send query param without manually typing url
# <a href="{% url 'search_api' %}?name={{ restaurant.restaurant_name }}"> Search similar </a> (For dynamic and)
# <a href="{% url 'search_api' %}?name=pizza">Search Pizza</a> (general)


# My confusion on why Django CBV separate (ListView, CreateView) but why does DRF combines ListCreateAPI or RetrieveUpdateDestroy

# super() calls the original version of a method from parent class so you dont have to rewrite everything, so we can 
# add own extra logic or modify results.

# Rules for hybrid CBV
# Order matters since python uses method resolution order (MRO) where first mixin on the left gets priority.
# e.g. class MenuListView(FormMixing,ListView): FormMixing goes first.
# When mixing you will need to override methods like post() because CBV doesnt know of post by default or modify the get_context_data,
# to add more variables to the template to generate.
# Mixing should be compatable, you cannot have two different post implementations without overriding. 
# Common Rule : have one main view (ListView,CreateView,UpdateView,DeleteView) and add optional mixins.
# Example of where mixing does not work:
# e.g. class ShiftView(ListView, CreateView)
# It will crash with the POST method because we call the CBV as a view using the .as_view() and what <as_view()> does is that it check if a method is
# inside of the say very last view (ListView in this case is the base class) it doesnt have a POST method so when django looks into the class for the POST
# it will crash and make an error. Even though the POST method is inside of the CreateView it wont get to it and will crash.

# HTTP requests are GET,POST,PUT, PATCH,DELETE
# HTTP responses consist of Body and status e.g. Body is the actual content that gets sent back to the client(browser) could be "JSON,HTML" 
# status means message from the backend or the codes sent by the server to the client the result of the request. (Status comes from the HTTP protocol).
# In CBV or general vies for DRF these statuses are set automatically but in Custom API, Custom FBV they need to be set manually.
# Common status codes : Get : 200, Post create 201, Delete 204, Not Found 404
# Status code groups:
# 2xx means success, 3xx redirects, 4xx client errors, 5xx server errors

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

# Difference between assinging foreign keys fields e.g. form.instance.employee = staff_object and form.instance.employee_id = 3
# In restaurant reservation we have the restaurant mentioned in the field while for the shift individual we dont have the employee id
# So we prefill the data here diff. In the assigning instace (form.instance.employee = staff_object) You pass actual object and django has 
# full object in memory more object oriented.
# < form.instance.employee_id = 3 > just pass the ID and django does not need the full object and its more direct and a bit 
# more efficent.
# A ForeignKey field stores only the ID (pk) in the database, but Django lets you either use a model instance or a raw primary key.
#  initial["restaurant"] = get_object_or_404(Restaurant, pk=restaurant_id) You are giving Django the Restaurant object and it
# converts it to .id when saving (Assigning a related object)
#  form.instance.employee_id = self.kwargs["pk"] assigning a raw foreign key value and Django does not have to fetch the staff object
# (Assigning a foreign key via primary key)

# For the Shift Case:
# Form does not have the employee field but you know the employee ID from url and PK is assigned is clear and efficient.
# For the Individual Reservation Case:
# The form had the restaurant field and you want a readable object in context so fetching object is useful

######################################################____Home____######################################################
def home(request):
    return render(request, "home.html",{})

######################################################____Restaurant___######################################################
class RestaurantList(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"
    # Context object name allows to change the variable name which we use inside of the restaurant_list.html 
    # e.g. : <for restaurant in restaurants>
    # changes the query name to restaurants inside of the get_context_data 
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

    def get_initial(self):
        initial = super().get_initial()
        initial["capacity"] = 100
        return initial

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
        return get_object_or_404(Restaurant, pk = self.kwargs["pk"])


    # Delete View works almost the same as UpdateView but it retrieves ONE object using a pk and then it deletes it instead of updating it.
    # GET -> show confirmation page (doesnt show prefilled form with data ), POST -> DELETE object
class RestaurantDelete(DeleteView):
    model = Restaurant
    template_name = "restaurant_delete.html"
    success_url = reverse_lazy("restaurant_list")

    ##### API
    # DRF generic views
    # Create an API view that can LIST and CREATE restaurant (so gets us GET to return all restaurant and POST to create new restaurant)
    # GET request : 1. Queries all restaurants -> serialises (converts to JSON) -> returns the JSON
    # POST request : 1. Incoming JSON, Serialiser validates it, Creates a Restaurant Object, Saves to DB and returns the JSON response
    # Having a CBV mixed view is more risky than a GET POST DRF ListCreate
class RestaurantListCreateAPI(generics.ListCreateAPIView):
    # Work with all Restaurants objects from the DB
    queryset = Restaurant.objects.all()
    # Use this serialiser to convert data
    serializer_class = RestaurantSerialiser

    # HTTP method handlers in Django
    # My confusion if this is allows to have a delete function why have different DRF with different purposes?
    # You can but you shouldn't because of design, clarity and control. Also DRF are designed around resources and endpoints.(Collection, Detail endpoints)
    # Why does it appear on the Django page? DRF looks at the view and asks what HTTP methods are implemented here so we can show as buttons.
    # Main buttons to show : [GET,POST,PUT,PATCH,Delete]

    def delete(self, request, *args, **kwargs):
        Restaurant.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        return super().get_queryset().order_by("-date_opened")

class RestaurantRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    # This is just a description of the query not actual data, and its only fetched when needed using .get() .filter() serialization 
    # This is a lazy query that only hits the database when needed, "I am ready to fetch all restaurants but not yet" but query only with pk

    queryset = Restaurant.objects.all() 
    serializer_class = RestaurantSerialiser
    # This pk is used not because of the kwargs from the url, but the pk from the module Field name pk
    lookup_field = "pk"

    # Just returns a JSON
class HelloWorldView(APIView):
    # How does this get converted into a JSON if its not using serialisation?
    # Response from from rest_framework.response import Response automatically converts a Python dictionary into JSON without serialisation
    # GET is automatically activated when we open a API page
    def get(self,request):
        return Response({"message":"Hello World !!!!"})
    
# Not automatic like generics so it gives full control over logic
# Inherit from the APIView 
class RestaurantSearchView(APIView):

    # GET /api/restaurants/search/?name=pizza
    def get(self, request):

        name = request.query_params.get("name", "")

        if name:
            restaurants = Restaurant.objects.filter(restaurant_name__icontains=name)
        else:
            restaurants = Restaurant.objects.all()

        serializer = RestaurantSerialiser(
            restaurants,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST /api/restaurants/search/
    def post(self, request):

        serializer = RestaurantSerialiser(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE /api/restaurants/search/
    # DELETE /api/restaurants/search/?pk=5
    def delete(self, request):

        name = request.query_params.get("name")

        # Delete one restaurant
        if name:
            restaurants = Restaurant.objects.filter(restaurant_name = name)

            restaurants.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        # Delete all restaurants
        Restaurant.objects.all().delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
######################################################___Reservations___######################################################

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "create_reservation.html"
    success_url = reverse_lazy("restaurant_list")

    # Most CBV have a get_context_data
    # We want to display the name of the Restaurant inside the template
    # We sent the exact row of the Restaurant.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = get_object_or_404(Restaurant, pk = self.kwargs.get("restaurant_id"))
        return context

    # Purpose of get_initial (Comes from CreateView) is to provide default values to form before its shown.
    # Here we just say prefill the restaurant field with this specific restaurant.
    # super(). gets me the original version of this method from parent class. 
    def get_initial(self):
        initial = super().get_initial()
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            # 404 means not "Not Found" and it will show a page instead of crashing.
            initial["restaurant"] = get_object_or_404(Restaurant, pk=restaurant_id)
        return initial

    # get_form (comes from CreateView) is job is to build and return the form instance
    # Why not just remove the restaurant field from the reservation form? Because its a required field and without it it will 
    # create error.
    def get_form(self, form_class=None):
        """Hide the restaurant field if it is pre-filled."""
        form = super().get_form()
        # Checks if URL include the restaurant_id
        if self.kwargs.get("restaurant_id"):
            # Widget is how the field is displayed in HTML
            # forms.HiddenInput() user does not see the field but it still gets submitted to DB because of previous get_initial.
            form.fields["restaurant"].widget = forms.HiddenInput()

            form.instance.restaurant = get_object_or_404(Restaurant, pk = self.kwargs.get("restaurant_id"))
        return form
    
    def form_valid(self, form):
        form.instance.restaurant = get_object_or_404(Restaurant, pk = self.kwargs.get("restaurant_id"))
        
        return super().form_valid(form)
    
class ReservationListCreateAPI(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialiser

    def delete(self, *args,**kwargs):
        Reservation.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
    def get_queryset(self):
        return super().get_queryset().order_by("restaurant")

class ReservationRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialiser
    lookup_field = "pk"

######################################################___Menu List___######################################################
    
    #Hybrid CBV
    # The ListView allows to get all of the rows from the MenuItem.
    # FormMixing gives the ability to handle a form in the same view because normally a ListView doesnt handle forms and CreateView doesnt 
    # show a list.
    # So here we want to display all menu items and allow adding a new menu item on the same page.
class MenuListView(FormMixin, ListView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menu_list.html"
    success_url = reverse_lazy("menu_list")
    context_object_name = "menu_items"

    # Normally a ListView only passes the object_list (All MenuItem rows, but we also want to add a form on the same page,
    # so manually add it to the context.
    # <get_form>, <form_class> and <form_valid> is from the FormMixing.
    # kwargs is the extra contex from everywhere else
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context
    
    # ListView by itself only handles GET requests so i t can't process a submitted form.
    # FormMixing offers the tools to make a POST, you then wrote your own post method because ListView is a GET - only so now 
    # because of the form method = "POST" it now calls your post method we just created.
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        # Re render the exact page but with included invalid errors
        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().order_by(
            "restaurant",
            "date_added"
        )

class MenuListCreateAPI(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerialiser

    def delete(self, *args,**kwargs):
        MenuItem.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return super().get_queryset().order_by(
            "restaurant",
            "date_added")

class MenuItemRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerialiser
    
    def get_object(self):
        return get_object_or_404(
            MenuItem,
            name__iexact = self.kwargs["name"],
            restaurant__restaurant_name__iexact = self.kwargs["restaurant"]
        )

######################################################___Staff___######################################################

class StaffView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "staff_add.html"
    success_url = reverse_lazy("staff_list")

class StaffList(ListView):
    model = Staff
    template_name = "staff_list.html"
    context_object_name = "members_of_staff"

    def get_queryset(self):
        return super().get_queryset().order_by(
            "restaurant",
            "position") # Alphabetical order of the roles

class StaffUpdateView(UpdateView):  
    model = Staff
    form_class = StaffForm
    template_name = "staff_update.html"
    success_url = reverse_lazy("staff_list")

class StaffDelete(DeleteView):
    model = Staff
    template_name = "staff_delete.html"
    success_url = reverse_lazy("staff_list")

class StaffListCreateAPI(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerialiser

    def delete(self, *args, **kwargs):
        Staff.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return super().get_queryset().order_by("restaurant")

class StaffRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerialiser
    
    def get_object(self):
        return get_object_or_404(
            Staff,
            name__iexact = self.kwargs["name"],
            surname__iexact = self.kwargs["surname"]
        )

######################################################___Shift___######################################################

class ShiftView(CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = "shift.html"
    success_url = reverse_lazy("shift_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shift_form"] = self.get_form()
        return context
    
class ShiftListView(ListView):
    model = Shift
    template_name = "shift_list.html"
    context_object_name = "shifts"

    def get_queryset(self):
        return super().get_queryset().order_by(
                            "employee",
                            "start_time"
                            )

class IndividualShiftView(ListView):
    model = Shift
    template_name = "individual_shifts.html"
    context_object_name = "individual_user_shifts"

    def get_queryset(self):
        return Shift.objects.filter(employee = get_object_or_404(Staff, pk = self.kwargs['pk'])).order_by("start_time")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = get_object_or_404(Staff, pk = self.kwargs['pk'])
        return context
    
class AddIndividualShiftView(CreateView):
    model = Shift
    form_class = ShiftForEmployeeForm
    template_name = "add_individual_shift.html"
    success_url = reverse_lazy("staff_list")
    
        # Employee id is not present in the form.
        # This is a Shift method where you exclude field and set it in the background
    def get_form(self, form_class=None):

        get_object_or_404(Staff, pk=self.kwargs["pk"])

        form = super().get_form()
        # Because get_form gets calles for both GET and POST, We insert this pk into both the instances but the POST is the one that matters.
        form.instance.employee_id = self.kwargs["pk"]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = get_object_or_404(Staff, pk=self.kwargs["pk"])
        return context
 
class ShiftListCreateAPI(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerialiser

    def delete(self,*args,**kwargs):
        Shift.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return super().get_queryset().order_by("employee",
                                                "start_time")

class ShiftRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerialiser
    lookup_field = "pk"
    

######################################################___Other___######################################################


    # We are using a FBV because a CBV usually expects to work on mostly one model else it requires to modify it, so its much simpler to use a 
    # FBV to fully give us the flexibility.
    # The Purpose of this whole FBV is to allow to have two different forms of two different models under the same page and view.
    # The main problem that could occur is the fact that say when we submit the form for restaurant it sends the data inserted by user to the validation
    # and it would pass but that same data would be sent to the menu form as well for validation and because menu doesnt have the same fields
    # as the restaurant it will fail validation and no row will be saved to both models. 
    # We use prefix to ensure we indicate which form its for. The name of the prefix doesnt matter because the model is known from the form.

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
        elif not menu_form.is_valid():
            print(menu_form.errors)
        
    else:
        restaurant_form = RestaurantForm(prefix = "restaurant")
        menu_form = MenuItemForm(prefix = "menu")

    return render(request, "combined_form.html",{
        "restaurant_form" : restaurant_form,
        "menu_form" : menu_form,
    })

#@login_required
#@permission_required('app.view_restaurant', raise_exception = True)
def restaurant_general_list(request):
    context = {}
    
    if request.user.is_authenticated:
        context["restaurants"] = Restaurant.objects.all()
        context["user_info"] = request.user.username
    else:
        context["notice_message"] = "Secret Test"
        context["user_info"] = "Unknown"
    
    return render(request,"restaurant_general_list.html",context)

@login_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id = restaurant_id)
    context = {"restaurant" : restaurant}
    return render (request,"restaurant_detail.html",context)

########################################################################################## Role based backend

def register(request):

    if request.method == "POST":
        form = UserRoleCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]
            group = Group.objects.get(name = role)

            user.groups.add(group)

            messages.success(request, "Sucessfully Registered !")
            
            return redirect("login_page")
    else:
        form = UserRoleCreationForm()
    
    context = {"form" : form}

    return render(request,"register.html",context)

@login_required
def dashboard_router(request):

    if request.user.groups.filter(name = "Owner").exists():
        return redirect("owner_dashboard_home")
    
    elif request.user.groups.filter(name = "Supervisor").exists():
        return redirect("supervisor_dashboard_home")
    
    elif request.user.groups.filter(name = "Staff").exists():
        return redirect("staff_dashboard_home")
    
@login_required
def owner_dashboard_home(request):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have permission to access this page")

    context = {"user" : request.user}

    return render(request,"owner_templates/owner_home_page.html")

@login_required
def supervisor_dashboard_home(request):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to access this page")
    
    context = {"user" : request.user}

    return render(request, "supervisor_templates/supervisor_home_page.html", context)

@login_required
def staff_dashboard_home(request):

    if not request.user.groups.filter(name = "Staff").exists():
        return HttpResponseForbidden("You do not have permission to access this page")
    
    context = {"user" : request.user}

    return render(request, "staff_templates/staff_home_page.html", context)

############################################# Restaurant #############################################

@login_required
def display_all_restaurants(request):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have permission to access this page")
    
    restaurants = request.user.restaurants_owned.all()
    context = {"restaurants" : restaurants}

    return render(request, "restaurant_templates/restaurant_list.html", context)

@login_required
def add_new_restaurant(request):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have permission to access this page")
    
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            # Commit=False means it creates the Restaurant instance but does not save it yet
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request,"New restaurant added succesffuly !")
            return redirect("display_all_owned_restaurants")

    else: 
        form = RestaurantForm()

    context = {"form" : form}

    return render(request, "restaurant_templates/restaurant_add.html",context)

@login_required
def delete_restaurant(request, restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have the permission to delete a restaurant.")

    restaurant = get_object_or_404(Restaurant,pk = restaurant_pk, owner = request.user)


    if request.method == "POST":
        
        restaurant.delete()
        messages.success(request, f"{restaurant.restaurant_name} has been deleted!")
        return redirect("display_all_owned_restaurants")
    
    context = {"restaurant" : restaurant}

    return render(request, "restaurant_templates/restaurant_delete.html",context)

@login_required
def update_restaurant(request,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("No permission to modify restaurant")
    
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)

    if request.method == "POST":
        form = RestaurantForm(request.POST, instance = restaurant)
        if form.is_valid():
            restaurant = form.save(commit = False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request,f'{restaurant.restaurant_name} has been updated.')
            return redirect("display_all_owned_restaurants")
    else:
        form = RestaurantForm(instance = restaurant)

    context = {"form" : form,
               "restaurant" : restaurant}

    return render(request, "restaurant_templates/restaurant_update.html", context)

@login_required
def restaurant_full_info(request,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have permission to view this restaurant")

    # Times :
    today = timezone.now().date()
    this_week = timezone.now() - timedelta(days= 7)
    this_month = timezone.now() - timedelta(days= 31)
    this_year = timezone.now() - timedelta(days = 365)    

    # Restaurant Info
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)
    restaurant_location = restaurant.get_location_display()
    restaurant_cuisine = restaurant.get_restaurant_cuisine_display()

    #Menu
    total_menu_items = len(restaurant.menu_items.all())

    # __date means ignore all time focus just on data
    # Earnings
    total_earned_from_orders = sum(order.total_price for order in restaurant.orders.all())
    today_earned = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__date = today))
    this_week_earned = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = this_week))
    this_month_earned = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = this_month))
    this_year_earned = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = this_year))
    # Orders Info:
    number_of_orders = len(restaurant.orders.all())
    orders_today = len(restaurant.orders.filter(date_time_of_order = today))
    orders_this_week = len(restaurant.orders.filter(date_time_of_order__gte = this_week))
    orders_this_month = len(restaurant.orders.filter(date_time_of_order__gte = this_month))
    orders_this_year = len(restaurant.orders.filter(date_time_of_order__gte = this_year))

    if total_earned_from_orders > 0 and number_of_orders > 0:
        average_transaction_cost = total_earned_from_orders // number_of_orders
    else:
        average_transaction_cost = 0

    # Labour Info:
    staff_count = len(restaurant.who_works_here.all())

    chief_staff = restaurant.who_works_here.filter(position = "chief")
    waiter_staff = restaurant.who_works_here.filter(position = "waiter")
    manager_staff = restaurant.who_works_here.filter(position = "manager")

    total_labour_hours = sum(staff.total_hours_worked for staff in restaurant.who_works_here.all())
    total_labour_hours_last_week = sum(staff.total_hours_worked_last_week for staff in restaurant.who_works_here.all())
    total_hours_worked_last_month = sum(staff.total_hours_worked_last_month for staff in restaurant.who_works_here.all())
    total_hours_worked_last_year = sum(staff.total_hours_worked_last_year for staff in restaurant.who_works_here.all())

    # Labour Costs
    total_labour_cost = sum(employee.total_earned for employee in restaurant.who_works_here.all())
    labour_cost_this_week = sum(employee.total_earned_this_week for employee in restaurant.who_works_here.all())
    labour_cost_this_month = sum(employee.total_earned_last_month for employee in restaurant.who_works_here.all())
    labour_cost_this_year = sum(employee.total_earned_last_year for employee in restaurant.who_works_here.all())

    # Food Permformance
    all_starters = restaurant.menu_items.filter( category = "starter" )
    number_of_starters = len(all_starters)
    number_of_starters_ordered = 0
    for starter in all_starters:
        for starter_ordered in starter.order_items.all():
            number_of_starters_ordered += starter_ordered.quantity


    all_mains = restaurant.menu_items.filter( category = "main" )
    number_of_mains = len(all_mains)
    number_of_mains_ordered = 0
    for main_ordered in all_mains:
        for order_item in main_ordered.order_items.all():
            number_of_mains_ordered += order_item.quantity
    

    all_deserts = restaurant.menu_items.filter( category = "dessert" )
    number_of_deserts = len(all_deserts)
    number_of_deserts_ordered = 0
    for desert in all_deserts:
        for desert_ordered in desert.order_items.all():
            number_of_deserts_ordered += desert_ordered.quantity

    all_drinks = restaurant.menu_items.filter( category = "drink" )
    number_of_drinks = len(all_drinks)
    number_of_drinks_ordered = 0
    for drink in all_drinks:
        for drink_ordered in drink.order_items.all():
            number_of_drinks_ordered += drink_ordered.quantity
        
    all_snacks = restaurant.menu_items.filter( category = "snack" )
    number_of_snacks = len(all_snacks)
    number_of_snacks_ordered = 0
    for snack in all_snacks:
        for snack_ordered in snack.order_items.all():
            number_of_snacks_ordered += snack_ordered.quantity
        
    category_sales = {
        "Starter": number_of_starters_ordered,
        "Main": number_of_mains_ordered,
        "Dessert": number_of_deserts_ordered,
        "Drink": number_of_drinks_ordered,
        "Snack": number_of_snacks_ordered,
    }

    most_popular_category = max(
        category_sales,
        key = category_sales.get
    )

        
    total_items_sold = (
    number_of_starters_ordered
    + number_of_mains_ordered
    + number_of_deserts_ordered
    + number_of_drinks_ordered
    + number_of_snacks_ordered
        )
    
    if total_items_sold > 0:
        starters_percent = (number_of_starters_ordered / total_items_sold) * 100
        mains_percent = (number_of_mains_ordered / total_items_sold) * 100
        desserts_percent = (number_of_deserts_ordered / total_items_sold) * 100
        drinks_percent = (number_of_drinks_ordered / total_items_sold) * 100
        snacks_percent = (number_of_snacks_ordered / total_items_sold) * 100
    else:   
        starters_percent = 0
        mains_percent = 0
        desserts_percent = 0
        drinks_percent = 0
        snacks_percent = 0
        
    starter_revenue = 0
    for starter in all_starters:
        for starter_ordered in starter.order_items.all():
            starter_revenue += starter_ordered.total_cost


    main_revenue = 0
    for main in all_mains:
        for main_ordered in main.order_items.all():
            main_revenue += main_ordered.total_cost


    dessert_revenue = 0
    for dessert in all_deserts:
        for dessert_ordered in dessert.order_items.all():
            dessert_revenue += dessert_ordered.total_cost


    drink_revenue = 0
    for drink in all_drinks:
        for drink_ordered in drink.order_items.all():
            drink_revenue += drink_ordered.total_cost


    snack_revenue = 0
    for snack in all_snacks:
        for snack_ordered in snack.order_items.all():
            snack_revenue += snack_ordered.total_cost

    category_revenue = {
        "Starter": starter_revenue,
        "Main": main_revenue,
        "Dessert": dessert_revenue,
        "Drink": drink_revenue,
        "Snack": snack_revenue,
    }

    highest_earning_category = max(
        category_revenue,
        key = category_revenue.get
    )

    lowest_earning_category = min(
        category_revenue,
        key = category_revenue.get
    )
    
    # Reservations
    all_reservations = restaurant.reservations.all()
    reservations_for_today = restaurant.reservations.filter(reservation_date_time__date = today)
    reservations_this_week = restaurant.reservations.filter(reservation_date_time__gte = this_week)
    reservations_this_month = restaurant.reservations.filter(reservation_date_time__gte = this_month)
    reservations_this_year = restaurant.reservations.filter(reservation_date_time__gte = this_year)

    active_reservations = restaurant.reservations.filter(is_active = True)
    inactive_reservations = restaurant.reservations.filter(is_active = False)



    context = {# General Information :
               "restaurant" : restaurant, 
               "restaurant_location" : restaurant_location,
               "restaurant_cuisine": restaurant_cuisine,

                # Finances
                "average_transaction_cost" : average_transaction_cost,
                "total_earned_from_orders" : total_earned_from_orders,
                "today_earned" : today_earned,
                "this_week_earned" : this_week_earned,
                "this_month_earned" : this_month_earned,
                "this_year_earned" : this_year_earned,

                # Orders : 
                "number_of_orders" : number_of_orders,
                "orders_today": orders_today,
                "orders_this_week" : orders_this_week,
                "orders_this_month" : orders_this_month ,
                "orders_this_year" : orders_this_year,

                # Menu 
                "total_menu_items" : total_menu_items,

                # Labour Info
                "staff_count" : staff_count,
                "chief_count" : chief_staff.count(),
                "waiter_count" : waiter_staff.count(),
                "manager_count" : manager_staff.count(),

                "total_labour_hours" : total_labour_hours,
                "total_labour_hours_last_week" : total_labour_hours_last_week,
                "total_hours_worked_last_month" : total_hours_worked_last_month,
                "total_hours_worked_last_year" : total_hours_worked_last_year,

                # Labour Cost
                "total_labour_cost": total_labour_cost,
                "labour_cost_this_week": labour_cost_this_week,
                "labour_cost_this_month" : labour_cost_this_month,
                "labour_cost_this_year" : labour_cost_this_year,

                # Food Information
                "most_popular_category" : most_popular_category,
                "highest_earning_category" : highest_earning_category,
                "lowest_earning_category" : lowest_earning_category,
                "number_of_starters": number_of_starters,
                "number_of_starters_ordered": number_of_starters_ordered,
                "number_of_mains": number_of_mains,
                "number_of_mains_ordered": number_of_mains_ordered,
                "number_of_deserts": number_of_deserts,
                "number_of_deserts_ordered": number_of_deserts_ordered,
                "number_of_drinks": number_of_drinks,
                "number_of_drinks_ordered": number_of_drinks_ordered,
                "number_of_snacks": number_of_snacks,
                "number_of_snacks_ordered": number_of_snacks_ordered,

                "starters_percent": starters_percent,
                "mains_percent": mains_percent,
                "desserts_percent": desserts_percent,
                "drinks_percent": drinks_percent,
                "snacks_percent": snacks_percent,

                # Reservations
                "number_of_total_reservations": all_reservations.count(),
                "reservations_today": reservations_for_today.count(),
                "reservations_this_week": reservations_this_week.count(),
                "reservations_this_month": reservations_this_month.count(),
                "reservations_this_year": reservations_this_year.count(),
                "active_reservations" : active_reservations.count(),
                "inactive_reservations" : inactive_reservations.count()
                }



    return render(request, "restaurant_templates/restaurant_info.html",context)

############################################# Staff #############################################

@login_required
def display_all_staff(request):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to view Staff")
    
    restaurant_staff = {}

    if request.user.groups.filter(name = "Owner").exists():

        all_restaurants = Restaurant.objects.filter(owner = request.user)

        for restaurant in all_restaurants:
            restaurant_staff[restaurant] = restaurant.who_works_here.all()
        
    elif request.user.groups.filter(name = "Supervisor").exists():

        all_staff = Staff.objects.filter(manager = request.user)

        for staff in all_staff:
            restaurant_staff.setdefault(staff.restaurant, []).append(staff)

    context = {
            "restaurant_staff" : restaurant_staff
        }

    return render(request,"staff_templates/staff_list.html",context)

@login_required
def delete_staff(request,staff_pk):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists() :
        return HttpResponseForbidden("You do not have the permission to delete a memeber of staff")
    
    staff = get_object_or_404(Staff,pk = staff_pk)

    if request.method == "POST":
        staff.delete()
        messages.success(request,f'{staff.name} was fired from {staff.restaurant.restaurant_name}')
        return redirect("display_all_staff")

    context = {"staff" : staff}

    return render(request,"staff_templates/staff_delete.html",context)

@login_required
def add_staff(request):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to add new staff.")

    is_owner = request.user.groups.filter(name = "Owner").exists()
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

    if is_owner:

        if request.method == "POST":

            form = StaffForm(request.POST)

            if form.is_valid():
                form.save()
                name = form.cleaned_data["name"]
                surname = form.cleaned_data["surname"]
                restaurant = form.cleaned_data["restaurant"]
                messages.success(request, f'{name} {surname} was hired at {restaurant}.')
                return redirect("display_all_staff")
        else:

            form = StaffForm()

        context = {
            "form" : form
        }

        return render(request, "staff_templates/staff_add.html",context)
    
    elif is_supervisor:

        if request.method == "POST":

            form = StaffFormSupervisor(request.POST)

            form.instance.manager = request.user

            if form.is_valid():
                form.save()
                name = form.cleaned_data["name"]
                surname = form.cleaned_data["surname"]
                restaurant = form.cleaned_data["restaurant"]
                messages.success(request, f'{name} {surname} was hired at {restaurant}.')
                return redirect("display_all_staff")
        else:

            form = StaffFormSupervisor()
        
        context = {
            "form" : form
        }

        return render(request, "staff_templates/staff_add.html",context)
        



@login_required
def staff_info(request, staff_pk):
    
    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to Access Staff Info")
    
    staff = get_object_or_404(Staff, pk = staff_pk)

    context = {
        "staff" : staff
    }

    return render(request,"staff_templates/staff_info.html",context)

@login_required
def update_staff_info(request, staff_pk):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have access to Update Staff Info")
    

    is_owner = request.user.groups.filter(name = "Owner").exists()
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

    staff = get_object_or_404(Staff, pk = staff_pk)

    if is_owner:
        
        if request.method == "POST":
            form = StaffForm(request.POST, instance = staff)
            if form.is_valid():
                form.save()
                messages.success(request, f'Sucessfully updated {staff.name} info.')
                return redirect("staff_info", staff_pk = staff.pk)
        else:
            form = StaffForm(instance = staff)
        
        context = {
            "staff" : staff,
            "form" : form
        }

        return render(request,"staff_templates/staff_update.html",context)
    
    elif is_supervisor:

        if request.method == "POST":
            form = StaffFormSupervisor(request.POST, instance = staff)
            if form.is_valid():
                staff = form.save(commit = False)
                staff.manager = request.user
                staff.save()
                messages.success(request,f'Sucessfully updates {staff.name} info.')
                return redirect("display_all_staff")
        else:
            form = StaffFormSupervisor(instance = staff)

        context = {
            "staff" : staff,
            "form" : form
        }

        return render(request, "staff_templates/staff_update.html", context )


############################################# Menu Item #############################################

@login_required
def display_all_restaurant_and_menuitems(request):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor"):
        return HttpResponseForbidden("You do not have acess to View Restaurant Menu Items")

    if request.user.groups.filter(name = "Owner").exists():
        all_owned_restaurants = Restaurant.objects.filter(owner = request.user)
        role = "Owner"
    elif request.user.groups.filter(name = "Supervisor").exists():
        all_owned_restaurants = Restaurant.objects.filter(supervisor = request.user)
        role = "Supervisor"

    restaurant_menu_items = {}

    for restaurant in all_owned_restaurants:
        restaurant_menu_items[restaurant] = restaurant.menu_items.all()
    
    context = {
        "restaurant_menu_items" : restaurant_menu_items,
        "role" : role
    }

    return render(request, "menu_templates/restaurant_menu_list.html",context)

@login_required
def add_new_menu_item(request,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have permission to Add new menu Item")
    
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    # Because of the validator which needs the restaurant field we need to set the instance restaurant instead after validating
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        form.instance.restaurant = restaurant
        if form.is_valid():
            form.save()
            messages.success(request,f'Sucessfully added for {restaurant.restaurant_name}')
            return redirect("list_restaurants_menu_items")
    else:
        form = MenuItemForm()

    context = {
        "restaurant" : restaurant,
        "form"  : form
    }

    return render(request,"menu_templates/add_menu_item.html",context)

@login_required
def delete_menu_item(request,menu_item_pk,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do no have permission to delete menu item.")
    
    menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
    restaurant = get_object_or_404(Restaurant,pk = restaurant_pk)

    if request.method == "POST":
        menu_item.delete()
        messages.success(request,f'Sucessfully removed {menu_item.name} from {restaurant.restaurant_name}s menu list !')
        return redirect("list_restaurants_menu_items")

    context = {
        "restaurant" : restaurant,
        "menu_item" : menu_item
    }

    return render(request,"menu_templates/delete_menu_item.html",context)

@login_required
def menu_item_info(request,menu_item_pk,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to check menu item information")
    
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
    menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)

    form = MenuItemForm(instance = menu_item)
    form.instance.restaurant = restaurant

    context = {
        "restaurant" : restaurant,
        "menu_item" : menu_item,
        "form" : form
    }

    return render(request, "menu_templates/menu_item_info.html",context)

@login_required
def update_menu_item(request,menu_item_pk,restaurant_pk):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You do not have access to Update Menu Items")
    
    menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance = menu_item)
        form.instance.restaurant = restaurant
        if form.is_valid():
            form.save()
            messages.success(request,f"Sucessfully updated {menu_item.name}.")
            return redirect("list_restaurants_menu_items")
    else:
        form = MenuItemForm(instance = menu_item)
    
    context = {
        "menu_item" : menu_item,
        "restaurant" : restaurant,
        "form" : form
    }
    
    return render(request, "menu_templates/menu_item_update.html", context)

############################################# Shift #############################################

@login_required
def shift_list_brief(request):

    if not request.user.groups.filter(name = "Owner").exists():
        return HttpResponseForbidden("You have no permissions to view all shifts")
    
    all_shifts = Shift.objects.filter(employee__restaurant__owner = request.user).order_by("employee__restaurant","start_time")

    context = {
        "all_shifts" : all_shifts
    }

    return render(request, "shift_templates/shift_list.html",context) 

@login_required
def shift_list_full(request):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have acess to view the Shift List")
    
    all_staff = Staff.objects.filter(manager = request.user)

    all_staff_shifts = {}
    for staff in all_staff:
        all_staff_shifts[staff] = staff.shifts.all()
    
    context = {
        "all_staff_shifts" : all_staff_shifts
    }

    return render(request, "shift_templates/shift_list_supervisor.html",context)

@login_required
def add_shift(request, staff_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have acess to add new shifts")
    
    staff = get_object_or_404(Staff,pk = staff_pk)

    if request.method == "POST":
        form = ShiftForEmployeeForm(request.POST)
        form.instance.employee = staff
        if form.is_valid():
            shift = form.save(commit = False)
            shift.employee = staff
            shift.save()
            messages.success(request, f'Successfully added {staff.name} for a shift.')
            return redirect("shift_list_full")
    else:
        form = ShiftForEmployeeForm()

    context = {
        "form" : form,
        "staff" : staff
    }

    return render(request, "shift_templates/add_shift.html",context)

@login_required
def delete_shift(request,shift_pk,staff_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have access to delete a shift.")
    
    shift = get_object_or_404(Shift, pk = shift_pk)
    staff = get_object_or_404(Staff, pk = staff_pk)

    if request.method == "POST":
        shift.delete()
        messages.success(request, f'Successfully delete {staff.name} shift.')
        return redirect("shift_list_full")

    context = {
        "shift" : shift,
        "staff" : staff
    }

    return render(request,"shift_templates/delete_shift.html",context)

@login_required
def update_shift(request, shift_pk, staff_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to update a shift.")
    
    shift = get_object_or_404(Shift, pk = shift_pk)
    staff = get_object_or_404(Staff, pk = staff_pk)

    if request.method == "POST":
        form = ShiftForEmployeeForm(request.POST, instance = shift)
        if form.is_valid():
            shift = form.save(commit = False)
            shift.employee = staff
            shift.save()
            messages.success(request, f'Sucessfully updated {staff.name}s shift !')
            return redirect("shift_list_full")
    
    else:
        form = ShiftForEmployeeForm(instance = shift)
    
    context = {
        "form" : form,
        "shift" : shift,
        "staff" : staff
    }

    return render(request, "shift_templates/update_shift.html", context)

############################################# Reservations #############################################

@login_required
def display_all_reservations(request):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to view reservations")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    
    all_restaurants = Restaurant.objects.filter(supervisor = request.user)

    all_reservations = {}

    for restaurant in all_restaurants:
        all_reservations[restaurant] = restaurant.reservations.all().order_by("reservation_date_time")
        
    context = {
        "is_supervisor": is_supervisor,
        "all_reservations" : all_reservations
    }

    return render(request, "reservation_templates/reservation_list.html",context)

@login_required
def add_reservation(request,restaurant_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have access to adding reservations")
    
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk )

    if request.method == "POST":
        form = ReservationForm(request.POST)
        form.instance.restaurant = restaurant
        if form.is_valid():
            reservation = form.save(commit = False)
            reservation.restaurant = restaurant
            reservation.save()
            messages.success(request,f'New reservation added to {restaurant.restaurant_name}')
            return redirect("reservation_list")
    else:
        form = ReservationForm()

    context = {
        "restaurant" : restaurant,
        "form" : form
    }

    return render(request,"reservation_templates/add_reservation.html",context)

@login_required
def delete_reservation(request, reservation_pk, restaurant_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to delete reservation")

    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    
    reservation = get_object_or_404(Reservation, pk = reservation_pk)
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, f'Deleted {reservation.name_of_reservation} reservation from {restaurant.restaurant_name}')
        return redirect("reservation_list")

    context = {
        "is_supervisor": is_supervisor,
        "reservation" : reservation,
        "restaurant" : restaurant,
    }

    return render(request, "reservation_templates/delete_reservation.html",context)

@login_required
def update_reservation(request, reservation_pk, restaurant_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("No permission to update reservation")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

    reservation = get_object_or_404(Reservation, pk = reservation_pk)
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance = reservation)
        form.instance.restaurant = restaurant
        if form.is_valid():
            reservation = form.save(commit = False)
            reservation.restaurant = restaurant
            reservation.save()
            messages.success(request,f'Sucessfully update the reservation at {restaurant.restaurant_name}')
            return redirect("reservation_list")
    else:
        form = ReservationForm(instance = reservation)
    
    form.instance.restaurant = restaurant

    context = {
        "is_supervisor" : is_supervisor,
        "reservation" : reservation,
        "restaurant" : restaurant,
        "form" : form
        }

    return render(request, "reservation_templates/update_reservation.html", context)

############################################# Order #############################################

@login_required
def order_list(request):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to look at the order list.")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

    all_restaurants = Restaurant.objects.filter(supervisor = request.user)

    restaurant_orders = {}

    for restaurant in all_restaurants:
        restaurant_orders[restaurant] = restaurant.orders.all().order_by("status","date_time_of_order")


    context = {
        "is_supervisor" : is_supervisor,
        "restaurant_orders" : restaurant_orders
   }

    return render(request, "order_templates/order_list.html",context)
    
@login_required
def add_order(request,restaurant_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to add a order")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    if request.method == "POST":
        form = OrderForm(request.POST, restaurant = restaurant)
        form.restaurant = restaurant
        if form.is_valid():
            order = form.save(commit = False)
            order.restaurant = restaurant
            order.save()
            messages.success(request, "Sucessfully added a new Order")
            return redirect("all_orders_list")

    else:
        form = OrderForm(restaurant = restaurant)
    
    form.instance.restaurant = restaurant

    context = {
        "is_supervisor" : is_supervisor,
        "restaurant" : restaurant,
        "form" : form
    }

    return render(request, "order_templates/add_order.html",context)

@login_required
def delete_order(request, order_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("No permission to delete order")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    order = Order.objects.filter(pk = order_pk)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Sucessfully delete an order")
        return redirect("all_orders_list")

    context = {
        "order" : order,
        "is_supervisor" : is_supervisor
    }

    return render(request, "order_templates/delete_order.html",context)
    

############################################# Order Items #############################################

@login_required
def add_order_items(request,order_pk,restaurant_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to add item to order")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    order = get_object_or_404(Order, pk = order_pk)
    restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

    if request.method == "POST":
        form = OrderItemForm(request.POST, restaurant = restaurant)
        form.instance.order = order
        if form.is_valid():
            order_item = form.save(commit = False)
            order_item.order = order
            messages.success(request, "Sucessfully added new item to order !")
            return redirect("all_orders_list")
    else:
        form = OrderItemForm(restaurant = restaurant)
    
    form.instance = order
    
    context = {
        "order" : order,
        "restaurant" : restaurant,
        "form" : form,
        "is_supervisor" : is_supervisor
    }    

    return render(request, "order_templates/order_items_templates/add_items.html",context)

@login_required
def list_all_order_items(request,order_pk):

    if not request.user.groups.filter(name = "Supervisor").exists():
        return HttpResponseForbidden("You do not have permission to add item to order")
    
    is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
    order = get_object_or_404(Order, pk = order_pk)

    all_items_by_category = {}
    for item in order.items.all():
        category = item.menu_item.category

        if category not in all_items_by_category.keys():
            all_items_by_category[category] = []
        
        all_items_by_category[category].append(item)

    context = {
        "is_supervisor" : is_supervisor,
        "order" : order,
        "all_items_by_category" : all_items_by_category
    }

    return render(request, "order_templates/order_items_templates/all_items.html",context)