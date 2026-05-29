from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Staff, Shift, MenuItem, Reservation
from .forms import RestaurantForm, MenuItemForm, StaffForm, ShiftForm, MenuItemForm, ReservationForm,ShiftForEmployeeForm
from .serialisers import RestaurantSerialiser, ReservationSerialiser, StaffSerialiser, ShiftSerialiser, MenuItemSerialiser
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy

from rest_framework import generics,status
from rest_framework.response import Response
# Create custom API views
from rest_framework.views import APIView

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
    
# Understand
# Not automatic like generics so it gives full control over logic
# Inherit from the APIView 
class RestaurantSearchView(APIView):
    # Runs when get request, it runs when we open the Rest API page
    def get(self, request):
        # Did the user send something called a name? if not then not then empthy by default 
        # query_params gets us anything after the defined URL so for < /restaurant/search?name=pizza&page=2 > 
        # restaurant/search used for Django routing and the query params is after ? so name=pizza&page=2
        name = request.query_params.get("name","")

        # If user provided a search value then find restaurants where name contains the search value
        if name:
            restaurants = Restaurant.objects.filter(restaurant_name__icontains = name)
        # Else return everything 
        else:
            restaurants = Restaurant.objects.all()
        
        # Converts Datao objects -> Python -> JSON-ready (Python dictionary )
        # My confusion is how does many = True works if we do pass a query_param ? would it not crash since its one instace?
        # .filter returns a query set (so a list of objects) so even if its just one object many = True works because its a list. 
        serializer = RestaurantSerialiser(restaurants, many = True)
        # Send JSON back to the browser (Client)
        # status.HTTP_200_OK tells the client that the request succeeded
        return Response(serializer.data, status = status.HTTP_200_OK)
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
        return form
    
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
    
    # ListView by itself only handles GET requests so it can't process a submitted form.
    # FormMixing offers the tools to make a POST, you then wrote your own post method because ListView is a GET - only so now 
    # because of the form method = "POST" it now calls your post method we just created.
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        # Re render the exact page but with included invalid errors
        return self.get(request, *args, **kwargs)

class MenuListCreateAPI(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerialiser

    def delete(self, *args,**kwargs):
        MenuItem.objects.all().delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return super().get_queryset().order_by("restaurant")

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
        return super().get_queryset().order_by("employee")

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
        return super().get_queryset().order_by("employee")

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