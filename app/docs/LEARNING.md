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

## Main Request lifecycle methods:
< get_queryset() > : Controls what objects are retrieved from DB (ListView, DRF generics)
< get_object() > : Controls how ONE object is retrieved (UpdateView,DeleteView,DetailView,RetriveAPIview)
< get_context_data() > : Extra variables to template.
< get_initial() > : Prefill form default before rendering
< get_form() > : Modify form object before validation,rendering (Hide fields, inject FK, disable fields, dynamic forms)  

# Purpose of __init__ in folders
When Python sees __init__.py inside a folder it understands that this folder containts python code that can be treated as a package, so files inside it can be imported else where. For example the reason we can do from app.models import Restaurant.
This files/modules inside a package inside it can be imported elsewhere.

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