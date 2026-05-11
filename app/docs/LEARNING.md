**You need markdown extension to process and format the markdown text.**

# Interpreter : A program that read and executes code/commands
# Hanging : A process appears to be stuck or unresponsive

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

# Deployment:
Acorn : is a tool/platform for packaging and deploying applications on the cloud. An acord file Acornfile defines how the app runs, 
servives/databases needed and ports/environment variables. (Deployment Instructions) Allows to give others our project with the acorn image

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
Use /app as the current working folder (cd /app) 
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

# Acorn
Problem with Kubernetes is that its very complicates with many elements and infrastructure setup. Acorn simplifies this by letting you define your app in a simpler way with [Containers, Servives, Jobs, Images] inside of the AcornFile. Acorn then automatically translates that into Kubernetes infrastructure. 
So its a developer friendly deployment platform on top of kubernetes, it does not replace docker or kubernetes but it uses them
AcornFile : deployment configuration file that describes your entire application system.
Dockerfile describes how to build one container, AcornFile describes how the whole application should run together.
Acornfile explains : [What containers exist, what database / services, startuporder, env orders]
AcornFile sits above DockerFile and the Kubernets, its used to overide them or to simplify them.
We still need DockerFiles tho.
Why have Commands in both? In Docker file CMD describes default startup command but in acorns its the kubernet deployment
The startup command in DockerFile always gets overriden by the acorn startup commands.

# Deployment commands
1. Ensure we are in the project which contains the AcornFile, DockerFile, manage.py and requirements.txt < ls >
2. Make sure that kubernetes works < kubectl get nodes > it should say :
   (venv) (base) cristiandumbravanu@Mac restaurant_project % kubectl get nodes
    NAME             STATUS   ROLES           AGE   VERSION
    docker-desktop   Ready    control-plane   75s   v1.32.2

### What does this mean 
Inside settings.py I added : 
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://*.on-acorn.io","https://*.on-acorn.io"]


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
4. Part 4 (Acorn)
   - Simplifies the deploying/managing the apps on Kubernetes
   - AcornFile describes the entire deployment application system 


# What is a Dockerfile:
A recipe for building an image and not running the container itself.
Image is like a frozen template / blueprint.
Container : live version of an image.

# Acorn File:
containers: {
  (Name of the container is web)
  web: {
    image: "python:3.12"

    build: {
      context: "."
    }

    ports: {
      publish: "8000:8000/http"
    }

    env: {
      DJANGO_SETTINGS_MODULE: "store.settings"
    }

    command: [
      "python",
      "manage.py",
      "runserver",
      "0.0.0.0:8000"
    ]
  }
}

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
Run docker run -p 8000:8000 restaurant-app:
