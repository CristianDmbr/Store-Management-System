**You need markdown extension to process and format the markdown text.**

# Interpreter : A program that read and executes code/commands
# Hanging : A process appears to be stuck or unresponsive

# Keep reusable global rule validators to just models.py for cleaner code which automatically gets put onto forms
# Forms does not activate the def clean() from models so just mention it inside of the serializer

# Validators that depend on a foreign key relationship are usually placed inside the model that owns or defines that foreign key relationship.
# The ORM lets Django treat database rows as Python objects and allows queries/comparisons between in-memory model objects and database data. (TRANSFORMS ROWS INTO ARRAYS OF PYTHON DICTIONARIES)

# save() is the very last function ran by Django after validating everything and before saving to DB.

# Prefill the field 2 ways:
Hidden prefilled form field : The field is included in the form, prefilled with a value using get_initial(), then hidden from the user with HiddenInput so it still gets submitted automatically.
Backend assignment model instance: The field is completely excluded from the form and instead assigned directly to form.instance before the model object is saved to the database.
1. Django creates a form instance using submitted form data.
2. The form instance internally creates and populates a temporary model instance.
3. The model instance is still only in Python memory and not saved to the database yet.
4. form.save() is what finally saves it to the database.

# Flow of forms instance and model instance
1. User submits data request.POST (containing raw strings)
2. Django creates a FORM instance (ShiftForm(request.POST) (validation object))
3. Form creates an interval model instance and its populated with validated data (Still not saved yet)
4. Get form runs After Django created the form instance but also before the final database save (So temporary model object exists and its populated with submited form data, but you can modify it before save happens)
5. You can modify the form.instance and then its form.save() to the database
   
# Serialisation
It converts any database row or input into a Python model object (Python array of python dictionaries) and the response turn it into JSON. So that's why model validation, ORM still works.

# Local Python object memory
My confusion is how does self.restaurant_name works for a row I am trying to create which does not exist in the database?
A model instance can exist in Python memory before it exists in the database.
There are two things : Python objects in memory and a actual database row.
When submiting a form, Django does not automatically save it DB but it first creates a dictionary instance which is a Python object, living in memory, not saved yet, its not a DB row yet but its an instance.
The self is never None since it always exists inside of function since Django already created a model object in Python memory, its the self.pk that is None because it has not been saved to database yet.
Forms does not work with database row dirrectly, it uses Python model objects.
Model is just a blue print used for Python model objects.
SERIALIZERS WORK THE SAME WAY AS FORMS.

# UPDATE single row with Python object memory:
Extract row from database and this row becomes a Python object, pass this object into form so instance = restaurant so it means update this object instead of create a new one. Django updates the same Python object so the object changes in memeory and this same object gets send for validation inside of the models.py.


# Why have validators with instance = None if theres always a instance?
Because we want validators to be reusable and some things like tests or shell scripts does not have instance.

# How does self work for both creatinga and updating if used inside of models.py ?
Both Create and Update use a model object in memory so in both cases self and self.restaurant_name works.
CREATE : user submits form data and Django created a new Python model object which exists inside Python memory, not in database yet but has no self.pk yet so when restaurant.clean() is ran self works because self is a temporary Python object.
UPDATE : Django first loads existing databse row, it then becomes a Python object, form updates it so restaurant.clean is ran again but with pk = 5

# Django forms:
Uses clean_<field_name> to automatically pass the parameter
# DRF serializers:
Uses  validate_<field_name> to automatically pass the parameter 

# self.instace
During every backend functionality we have a self.instance.
If its CREATE it internally automatically tries to extract a object which does not exist in the DB self.instance = Restaurant() which creates a EMPTY unsaved Python object so its pk is None.
For an UPDATE we extract the instance of pk.
This does not happen in ListView because it works with many objects.

# Validation
Enforced by Python not by DB.
If exists only in forms then APIs can bypass it. 
So its professional to centralize reusable validation into a validators.py inside of app.
Good validators.py logic is to have validators which can be used everywhere in the system meaning True on every level e.g. admin, forms, apis.
But things that are specifc to say API behaviour, user session should not be mentioned since they are specific

# What is the {% csrf_token %}?
- Inserts a hidden input input into the HTML form containing a protection of your form from submisions from malicious requests from other websites.

# What are migrations ?
- Migrations translate Python models into real database tables and fields and keeps database structure in sync with your code.
- Python @properties to the models do not require any migrations because only exists in the Python Memory and they do not change databse column so when you try to mitigate Django sees nothing to mitigate

(Extension used : Markdown All In One)

# What is a MarkDown? :
- A lightweight text formatting language that lets you write plain text and convert it into structured, styled documents (heading, lists or bold text).
- Text to HTML conversion tool for web writers.
- MarkDown is not a replacement for HTML, it only uses small elements so its very simple to use.
- The point of MarkDown is to help read and write.

# MarkDown Formations# :
- Heading 1, ## Heading 2, ### Heading 3
- For italics, ** Bold
- Unordered Lists *, +, - 
  -Ordered Lists 1 ... n

# APIs
What is an API : Is a way for programs to talk to each other.
What are they used for : send data, get data and connect apps. e.g. : Website asks backend for all restaurants so backend send it and they communicate through API.
How do they work? 
1. Cliend (browser/app) sends a request (Give me menu items)
2. Backend receives it, Django view, API processes it.
3. Backend sends a response (usually JSON) e.g. {"name" : "Pizza"}

Where  I could use it:
Right now: Django views return the HTML templates.

With APIs:
Django will return data (JSON) instead which allows for mobile apps, react frontends and other systems to use the backend.

# API POST flow:
(DRF serializers do not use Django Forms).
DRF serializers are the API equivalent of forms.
DJANGO HTML APP : Forms, HTML form input, Form Validation
DRF API: Serializers, JSON/API input, serializers validation

POST only uses One object so it uses serializers data = request.data instead of many = True since its just one object incoming

When a Client send a POST request DRF converts incoming request into request.data:
Wheater its JASON:
{
  "name" : "Pizza Place"
}
or HTML
name = Pizza+Place

it gets converted to request.data which behaives like a Python dictionary.

Serialization Validation Flow:
1. Raw request Data 2. Serialization.is_valid() 3. Field Validation 4. Custom Serializer Validation 5. Model instance
(Serializers validate before database save to catch errors)

The models.clean() or any custome field_validation that is inside models.py DOES NOT get automatically called because DRF serializers are independent validation systems



# Deployment:
DockerFile: Tells Docker how to build and run my Django Project

The flow : 
Docker will:
1. Create a mini isolated container/machine
2. Install Python
3. Install Dependencies (Requirements.txt)
4. Copy project files
5. Run Django server

Inside of the mysite folder I made a db-cript.sh (A shell script)
What is a shell script? A file containing terminal/Linux commands executed automatically
Mac terminal commands uses a Linux like system so they share the same commands. (So shell scripts are Linux/macOS oriented)

< 
#! /bin/bash
(This means shebang meaning, run this script using Bash (Bash is a Linux/terminal interpreter (Program that reads and executes code/commands) which understand commands))
(Bash is both a shell language and a command interpreter)
sleep 10
(Usually in Docker / deployment you may need time to start the database so the script waits before migrations run)

python3 manage.py makemigrations
(Make migrations means generate instructions describing database changes)
python3 manage.py migrate
(Apply those changes to the actual database) >

Why automate this? In deployment/container startup you want database setup to happend automatically (automatically meaning either executing the shell or when Docker when container starts ) instead of typing everytime. 
So its more of a startup checklist

Deployment : Putting your app onto a server so other people/devices can acess it.
Docker : Packages your app and all dependencies into an isolated container and dockerfile is instructions for building and running the container (e.g. install Python, copy project, install requirements, start server)

Docker = Shipping container
Docketfile = packing instructions
Deployment = shipping to public server
Running = turning the machine on 

# Inside my DockerFile
What problem is Docker solving? 
- My computer already has Python, pip, dependencies and terminal and the OS configuration but another computer/server may not. So if you move your project to another machine, it may fail because environment differs (e.g. Wrong Python version, missing packages)
- Docker says : "Lets package the ENTIRE environment"
- So docker creates isolated mini computers called "containers" and this container contains Python, dependency, your code and startup commands. 
What is a Dockerfile?
- A set of instructions for building a container
- Dockerfile uses a docker confifuration language not Python

- Docker file : Set of instructions of how to create your container
- Container : contains : Project and all code, Python, libraries etc..

< FROM python:3.12 >
Start from an existing Docker image (template for containers)
This isnt just the Python language its a prebuild env including linux filesystems, pip, shell.
This is a library from docker hub (Github for container images)

< WORKDIR /app > 
Inside of the container create and switch into folder called /app so this creates a folder inside of the container not related to the app folder inside my mac.

< COPY requirements.txt . > 
Copy the file from my computer to the container. (Docker containers starts empty and you must explicitly copy files into it)
"." Means copy file from current which is "/app" since we did < WORKDIR /app > 

< RUN pip install -r requirements.txt >
Install all dependencies into container, without this Django would not exist inside container

< COPY . . > 
Copies the entire Project into container

< EXPOSE 8000 >
This container inteds to use port 8000 (This is more documentation and doesnt do anything)

< CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] >
When container starts run this comments meaning python manage.py runserver 0.0.0.0:8000 meaning this runs Django.
This is important because containers only live while a process is running, so a container is an isolated running process.
CMD answers what process should I start when this container launches. 
Without CMD container starts, nuthing runs so containers exits.
Container needs one main active process which is the Django development server

# Kubernetes
Docker helps run one containerised application (e.g. Django app container) but real applications become bigger with a lot of elements (Django backend, Database) and managing many containers manually becomes difficult (Restarting crashes, updates )
Orcherstration : managing many containers automatically
Django : here are many containers
Kubernetes : Manage this entire application system (It can automatically start containers, restarts crashed contaiers etc...)
Without Kubernetes you manually run 10 containers but with it it runs automatically

Enabling Kubernets inside Docker created a local Kubernetes cluster on my machine
Cluster : group/environment where containers are orchestraed (So mac is now a mini cloud deployment server)

(A project has multiple containers where every container has a responsibility)

# Stack :
1. Part 1 (Django + DRF side)
   - Backend: Models,ORM,APIs,Database
   - Rest is an architerctural style for structuring APIs/resources and JSON is simply the most common response format.
   - Serializers converts Django model objects into Python dictionaries into lists and Response() converts them into a JSON body.
   - REST API page is the developer/testing interface not fronted UI.

2. Part 2 (Docker)
   - Docker : platform/tool for runnning and building containers. (Where images are created into containers)
   - DockerFile : How to build an image/environment
   - Container : A running isolated environment
   - DockerFile -> Image Built -> Image started -> Running Container

3. Part 3 (Kubernetes)
   - Kubernetes : automates orchestratration of many container, itself run inside cluster env
   - Cluster : The kubernetes environment
   - We have containers for every responsibility inside of project

# What is a Dockerfile:
A recipe for building an image and not running the container itself.
The commands like : FROM, WORKDIR, COPY, RUN, EXPOSE, CMD are all Dockerfile instructions and belong to the Docker syntax language
Image is like a frozen template / blueprint.
Container : live version of an image.

Python:3.12. Is an existing Docker image which already contains Linux,Python 3.12,pip and system tools.
COPY just means copy requirements.txt from your Mac into container current folder so it now becomes /app/requirements.txt inside the container.
EXPOSE does not actually open a port, its more for documentation
CMD command runs when the container starts.
BUILD PHASE : FROM, COPY, RUN    RUNTIME PHASE : CMD
CMD is necessary because containers live while their main process lives.

# 123.0.0.1 vs 0.0.0.0 
127 only accepts connections from INSIDE this env
while 0.0.0.0 accepts connections from ANY netwrk interface including Docker, external requests etc

# What is a PORT
computer = apartment building
IP adress = Which building
Port = which apartment/room
e.g. port gets you to django and the url gets you inside django
e.g. port is a numbered doorway
Port gets you to application, URL path handles inside of the application

# Commads : 
docker ps : which container uses my port
docker stop c7bc550291c3: stop container
docker images : all the images

# Server Logic
There are two servers involved : 1. My Mac 2. Django server inside of Django
When I run < docker run -p 8000:8000 restaurant-app >, it does not turn the Mac into Django.
Instead : Mac runs Docker, Docker runs containers and containers runs Django. So the Django server is inside of the container. 
Docker is like a Tiny Virtual Computer and the container is a mini isolated LinuxComputer inside my Mac.
Inside this mini computer : Python exists, Django exists, Requirements exists, Project exists and server runs.

When the Browser sends request to localhost : 8000 -> The mac receives the request -> Docker catches the request on Mac port 8000 -> Docker forwarfds the request into container -> Container port 8000 receives it -> Django responds -> Response goes back through Docker and Browser receives the HTML.
This means Mac does not directly run Django anymore its Docker who runs it.

Mac only: 
1. Hosting Docker
2. Forwards Traffic
3. Provides resources (CPU/RAM)
  
< docker run -p 8000:8000 restaurant-app >
what < -p 8000:8000 > means is HOST_PORT : CONTAINER_PORT 
Mac port 8000 forwards all requests to container port 8000

Every port has its own purpose e.g. 8000 Django

Why does browser still use localhost even if Docker runs it?
- Because Docker exposes the container to your machine meaning arriving at local host forwards to container.
- So Browser still talks to your mac but the Mac forwards traffic into Docker container.
- Browser does not know containers exists

# Running Docker:
registry inside of docker is the warehouse where the images are stored

<docker run -p 8000:8000 restaurant-app>
- run: Create and start a new container from an image
- -p : publish a port meaning forward traffic between host and container
- 8000:8000 from mac port 8000 to container port 8000
- restaurant-app is the image Name.
- docker stop cc8831d01683 : stops current docker container
- kubectl get nodes : checks the kubernetes nodes status

# Building the actual Docker Image:
<docker build -t restaurant-app .>

I first made the Docker File with instructions for container
I then entered < docker build -t restaurant-app .> which read the DockerFile, followed instructions, Created the Docker Image and named it restaurant-app (Created IMAGE not container). After you can run < docker run -p 8000:8000 restaurant-app > to create the container from this image.

# Does The image stay forever?
- Does the image need to be rebuild every time? No. Only if code, dependencies, dockerfile changes so then run < docker build -t restaurant-app . > 
- How does Docker find DockerFile? Docker automatically searches the directory for Dockerfile with exact name
- Can I delete the DockerFile after building? Yes because image already exists and this container contains all Python, dependencies, Djagno code, CMD and copied Files. 
  - BUT PROFESSIONALS DONT DO IT BECAUSE ITS SOURCE CODE AND DOCUMENTATION SO WITHOUT IT YOU CANT REBUILD SOMETHING LATER
  - One DockerFile usually describes one application/image so each project gets its own docker file
- Check for image list: <docker image ls>
- Check for running containers : <docker ps>

# Pass one URL Converter:
lookup_field = "pk"
  
# Pass more than one URL Converters
path("individual_staff/<str:name>/<str:surname>",StaffRetreiveUpdateDestroyAPI.as_view(), name = "staff_retrieve_update_destroy"),
<class StaffRetreiveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerialiser
    
    def get_object(self):
        return get_object_or_404(
            Staff,
            name__iexact = self.kwargs["name"],
            surname__iexact = self.kwargs["surname"]
        )>
    
# When passing more than one converter that is from a FK module:
def get_object(self):
        return get_object_or_404(
            MenuItem,
            name__iexact = self.kwargs["name"],
            restaurant__restaurant_name__iexact = self.kwargs["restaurant"]
        )

# get_form() Utilisation
( My Confusion was that get_form was used to get form during a GET request but also it can we used with .instance to modify during a POST request )
- get_form its used both on GET and POST requests. Its used for displaying forms but also when processing submitted forms.
Full Flow :
GET : 
1. User opens page GET /shift/5/add and CreateView CBV calls get_form(), 
2. Inside get_form() Django creates a form = super().get_form() (Empty form of ShiftFormEmployeeForm). And internally it makes a form.instance = Shift() which is a empty unsaved model object
3. The model instance gets modified < form.instance.employee_id = self.kwargs["pk"] > So now the temporary Shift Object has employee already attatched to it
4. Template renders the forms where only start_time, end_time and status is shown (Thats because we do not mention employee_id inside of the form.)
  
POST : 
1. CreateView is called again and it calles get_form() but with a request.POST
2. So this time it creates a form = ShiftForm(request.POST) 
 < form.instance = Shift(
    start_time=...,
    end_time=...,
    status=...
) > (Still not saved)
3. Override runs again < form.instance.employee_id = self.kwargs["pk"]> so this employee gets added before validation/save
4. Validation runs and the employee field is longer missing
With my example of : 
< def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Instance is the current form we want to save inside of the model.
        # This shift belongs to employee with pk from kwargs
        # Employee_id is automatically created by the foreign key relationship, so be careful with the naming.
        # But we could also just get the Emplyee object and assign it to the instance.employee = staff_object
        form.instance.employee_id = self.kwargs["pk"]
        return form > I have overrode for both POST and GET (Its most important during POST)

Why for < def get_form(self, form_class=None): > we mention form_class = None? 
If no custom form is passed, use the default self.form_class. 
Between < super().get_form(form_class) > and < form = super().get_form() > use second its more simple 

# Preffiling FK.
When filling the id field of a FK e.g. form.instance.employee_id = 5 we need the raw data < form.instance.employee_id = self.kwargs["pk"] >
But we could also do a Full object with form.instance.employee = get_object_or_404(Employee, pk = self.kwargs["pk"])
(Raw is a bit more efficient because it doesnt require extra DB query)


# Purpose of __init__ in folders
< __init__ > package initializer file
Its primarily for Python not Django.
When Python sees __init__.py inside a folder it understands that this folder containts python code that can be treated as a package, so files inside it can be imported else where. For example the reason we can do from app.models import Restaurant.
This files/modules inside a package inside it can be imported elsewhere.
So Python uses the initializer file to recognise a folder as a importable Python package/modules.
Package : A folder containing Python modules/files
A module : A single Python File

< Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'... >

Found 1 test means 1 test method inside it, Creating test database uses a temp isolated database. (The temporary test database is built using the same models, fields, migrations, and table structure as your real database.)
System check looks into all parts of Django : Models, URLs and so on. 0 silenced means no problems found.
<.> Each dot represents a test passed successfully
The last < OK > means all test passed
Then DB gets destroyed

1. Django found tests
2. Created temporary DB
3. Ran system checks
4. Executed tests
5. All passed
6. Deleted temporary DB

# Backend Architecture (Forms -> Model Instance -> Python Object Flow)
# GET request:
1. Calls get_form() to make an empty form object < form = RestaurantForm() > which: Renders HTML inputs, Users sees form
(An empty form object is created and an empty form.instance model object does exist but its not populated)


# POST request:
1. User sends a request.POST
2. A new Django form.instance is created < RestaurantForm(request.POST) > (This is a new instance that is different from the empty one from get_form during the GET request)
3. Inside of this form.instance we also create a empty python memory Model instance Restaurant() where the data to the fields are None
4. We can modify any sent POST request using get_form.instance to make changes or insert data into it before we send it to validate.
5. We call form.is_valid(): which will convert all string user input into Python data types ("50" to int 50), it will run clean_field(),clean().
6. If validation is successfull it will generate a cleaned_data() which is a Python dictionary of inputs converted into proper data types.
7. This cleaned_data() is copied inside of forms.instance() and inside of the emtpy Model instance Restaurant(cleaned_data).
8. form.save() is ran which then calls model.save() which takes this model instance with validated data, inserts/updates it into the database, which runs database constraints and saves it.


- Form instance : It contains fields from the model, validation rules, widgets, errors
- Cleaned_data : form_data after we validate the form.instance (A dictionary)
{
    "restaurant_name": "Pizza Palace",
    "capacity": 50
}
- Django model instance is a Python Object representing a database row so thats why we can do < form.instance.capacity >
  e.g. 
  restaurant = Restaurant(
    restaurant_name="Pizza Palace",
    capacity=50
)

# GET vs POST flow
GET : 
- View
- get_initial()
- get_form()
- get_context_data()
- template render

POST :
- View
- get_form()
- form_created using request.POST
- form.instance exists 
- validation
- form_valid()
- form.save()
- model_save()

# Modifying POST request :
1. Modify form.instance (Most Common)
  < form.instance.name = ... > (Professional and clean)
2. Modify the request data itself 
  < data = request.data.copy() 
    data["owner"] = request.user.id> (We have to copy the request.data because it can be imuttable sometimes, at the end return the copied/modified data)

# many = True
In DRF we have a many = True concept where we can make it so the serializer object expects more than one object, e.g. a queryset. 
Forms don't have this since it always expects only one object.

# serialzier.validated_data == form.cleaned_data

# Why does serializers have a Many = True?
Also why does a ListCreateAPIView use a serializer. DRF always works throught serializers. 
A serializer is used for BOTH GET list and POST create.

# GET DRF:
< restaurant = Restaurant.object.all()
  serializer = RestaurantSerializer(
    restaurants,
    many = True
  ) > 

< serializer.data >
[
    {
        "id": 1,
        "restaurant_name": "Pizza"
    }
]

# Does GET DRF validate eveyrthing? 
The reason we have a serializer is to convert Model Objects into Python Dictionaries to be used JSON.

# Serializer GET request Flow
1. Restaurant.objects.all()
2. Serializer used with < RestaurantSeriazlier(queryset, many = True) >
3. serializer.data is a Python List of dictionaries.
4. Response (seriazlier.data)
5. JSON gets sent to client

# POST DRF request Flow:
1. User sends JSON request.data
{
    "restaurant_name": "Pizza Palace",
    "capacity": 50
}
2. Create serializer using this data < serializer = RestaurantSerializer( data=request.data )>
No model instance yet, unlike ModelForms, serializers do not create an empty model instances immediately.
3. Validate using serializer.is_valid() which creates serializer.validated_date()
{
    "restaurant_name": "Pizza Palace",
    "capacity": 50
} equaivalent of form.cleaned_data
4. Save the serializer serializer.save()
5. Make a model instance 
  Restaurant.objects.create(
    **serializer.validated_data
)
5. save it.
6. After saving it take the model instance we just made and serialize it again to turn it back into a python dictionary which is serialzier.data
7. use this serialized.data to make a JSON response to show back to user.


# Difference between form request.data and serializer request.data which comes from POST
Django Forms : The user input of forms comes in a form of a Python dictionary where all the values are strings, these values are converte into Python types during is_valid() e.g. "50" to int 50
DRF : sends the data into the serializer as an already parsed from JSON to Python Objects using DRF's parse before validation starts.

# Serializer.data:
< {
    "id": 1,
    "restaurant_name": "Pizza Palace"
} >

# QuerySet
< restaurants = Restaurant.objects.all()

for restaurant in restaurants:
    print(restaurant.restaurant_name) > 

[
    Restaurant(
        restaurant_name="Pizza Palace",
        capacity=50
    ),
    Restaurant(
        restaurant_name="Burger House",
        capacity=100
    )
]

# Query Parameters 
URL : < /api/restaurants/search?name=pizza&location=london >
But the actual URL route is < api/restaurant/search >

How to Extract : 
- CBV or FBV: request.GET.get("name")
- DRF : request.query_params.get("name)

Purpose of URL converters : Identify a specific resource
Purpose of a query parameter : optional settings for filtering, searching, 

# Definition of < from .models import Restaurant >
Not importing the database rows but instead the model blueprint which contains the information of the fields and if its CharField,IntegerField etc...
Restaurant = blueprint
Restaurant.objects = managaer that can talk to a database
- My confusion is how does Django know whether to use the test database or the real database?
Normally Restaurant manager is connecteed to the production database so normally any <.objects> works on the production database.
But when we run < python manage.py test > it temporarily switches the connection from the real database to the test temporary database and once temporary database is destroyed, it reconnects back to the original database.

# An aware datetime knows the timezone its in but < datetime(2022, 2, 2, 22, 10) > is a naive datetime which does not know the timezone (Only applies to datetime not date)
aware date time < timezone.make_aware(datetime(2022,2,2,22,10)) >
naive datetime < datetime(2022,2,2,22,10) >

# timezone.now() vs datetime.now() 
Both are date time fields but the timezone is imported from djago.utils which makes an aware datetime.
datetime is imported from datetime

# Time delta
timedelta() can be used to modify a datetime field with either days = 1 or hours = 10

# My worry with testing was that I only have assertEqual() assertRaises() assertTrue() assertFalse().
These assertions are 80% - 90% of the Django testing.

# date.today() datetime.now()

# Accessing rows while being a FK
Suppose you have :
< class Shift(models.Model):
    employee = models.ForeignKey(
        Staff,
        related_name="shifts",
        on_delete=models.CASCADE
    ) >
Doing staff.shifts doesnt bring the shifts themselves but its a UI related manager to query. e.g. :
staff.shifts.all()
staff.shifts.filter()

# What is self.client()
When Django creates a TestCase (e.g. RestaurantViewTests(TestCase)) it automatically creates a < self.client > which represents a fake browser. So instead of having a Real Browser asking requests of the URL router we have the Django Test Client communicationg to the url router similar to how we have a temporary DB inside a TestCase.
With this self.client we can also do a POST.
GET : 
< response = self.cient.get(reverse("restaurant_list")) >
Push : 
< response = self.client.post(reverse("restaurant_add"),{"restaurant_name" : kfc, ...}) >

# Purpose of reverse("restaurant_list")
It convets "restaurant_list" into "/restaurants/".
Using the url router it will return < "/restaurants/" >
The client sends GET "/restaurants/" to Django and it finds the path with the RestaurantList.as_view().
Django then executes the RestaurantList and this view returns a Django HttpResponse object containing :
- status_code : 200
- content : rendeted HTML
- context : {"restaurants" : < queryset >}
- templates = [""restaurant_list.html]

# self.assertTemplateUsed checks if the Http response used the template, not if the template equals the response.

# Why not import a CBV for testing?
Users dont do RestaurantList() instead it they call GET /restaurant/ so the tests should do the same.
  
# Status_code
Every HTTP response contains a status code.
Easy memory trick :
2xx = Sucess
3xx = Redirect
4xx = User Problem
5xx = Programmer Problem

# What is happening in :
<  def test_restaurant_list_contains_restaurants_pass(self):

        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertIn(self.restaurant, response.context["restaurants"]) >
1. This TestCase creates a temporary database with real database rows inside.
2. Client makes a request so the name of url "restaurant_list" gets converted to a real URL request GET /restaurants/ just like a browser.
3. In the URL router it executes RestaurantList
4. The CBV queries the TEST database with get_queryset() from the temporary database.
5. This query set is placed inside get_context which gets passed to the template to show as restaurants because of related_object_name. 
6. Template received the context with the query set and is kept within the response.context["restaurants"]
7. We compare if our Model instance self.restaurant object is within this queryset of other model instance objects. 
   
# Idea of having tests inside of unit tests
We can have multiple self.asserts under the same unit test if its under the same behaviour. e.g. :
<     def test_restaurant_age_are_ordered_by_date_opened_descending_pass(self):
        
        older_restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Old Restaurant",
            date_opened=date(2020, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
            )

        newer_restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="New Restaurant",
            date_opened=date(2025, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
            )
        
        response = self.client.get(reverse("restaurant_list"))
        restaurants = list(response.context["restaurants"])

        self.assertEqual(self.restaurant,restaurants[0])
        self.assertEqual(newer_restaurant, restaurants[1])
        self.assertEqual(older_restaurant, restaurants[2]) >
    
# self.assertIsInstance
It can be used to check if a response from the server has the instance of a form.
<     def test_restaurant_create_uses_restaurant_form(self):
        response = self.client.get(reverse("restaurant_create"))
        self.assertIsInstance(response.context["form"],RestaurantForm) >
  
# Check amount of rows in a Database:
< Restaurant.objects.count() >

# Redirect success_code = 302

# Failed POST request
If a POST request fails status code will be 200 because it has failed and curr page will reload again with error.

# Reverse a Update/Delete request
Because the URL path contains URL parameters when a client makes a url request it must have :
         < response = self.client.get(reverse("restaurant_edit",
                                    kwargs = {"pk" : self.restaurant.pk})) > 
That is only because we mention the pk in the URL parameter list : 
        < path("restaurant/<int:pk>/edit",views.RestaurantUpdate.as_view(), name = "restaurant_edit"), > 
  
# UpdateView
It uses the form to display data by taking the object and converting into form fields to populate the HTML inputs, this comes from from.instance. 
form.instance is the actual model object instance and not the cleaned_data.
This is because when we use GET request to an UpdateView Django already has the model object no need to convert to a Python dictionary to display like the serializers because tehre you cannot send Django model objects over HTTP. 

# In APIs, we do not expose Django model objects directly. Instead, we retrieve model instances from the database, serialize them into Python dictionaries, and then convert those dictionaries into JSON for transmission to the client.

# Reverse() needs to also contain url parameters
# Check if the redirect of a response is correct
< self.assertRedirects(response, reverse("restaurant_list")) >

# self.restaurant.refresh_from_db() 
Updates any objects in memory after changes to the database. e.g. after updating a row and wanting to get the new updated name.

# Delete view 
Django automatically passes the Django instance object as context["object"] = Django model instance

# Check if a redirection was to the correct template
< self.assertRedirects(response,reverse("restaurant_list")) >
response is a HTTPResponseRedirect status_code = 302 and the reverse is a string URL.

# CBV created 302, API created 201

## Main Request lifecycle methods:
< get_queryset() > : Controls what objects are retrieved from DB (ListView, DRF generics)
< get_object() > : Controls how ONE object is retrieved (UpdateView,DeleteView,DetailView,RetriveAPIview)
< get_context_data() > : Extra variables to template.
< get_initial() > : Prefill form default before rendering
< get_form() > : Modify form object before validation,rendering (Hide fields, inject FK, disable fields, dynamic forms)  