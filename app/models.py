from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('almost_done', 'Almost Done')
    ]

    user = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = "tasks"
    )

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default = False)
    assistance = models.CharField(max_length = 200, null = True, blank = True)
    date_created = models.DateTimeField(default = timezone.now)
    due_date = models.DateTimeField(null = True, blank = True)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'not_started'
    )

    def __str__(self):
        return self.title

from django.shortcuts import render,redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # 🔥 THIS LINE
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/task_list.html",{
        "tasks":tasks,
        "form" : form,
    })

def complete_task(request, task_id):
    task = Task.objects.get(id = task_id)
    task.completed = True
    task.save()
    return redirect("task_list")


def delete_task(request, task_id):
    # Safely get the task or return a 404 page if it doesn't exist
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")

def all_tasks(request):
    tasks = Task.objects.all().order_by("-id")
    return render(request, "tasks/all_tasks.html", {"tasks" : tasks})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html",{"form": form})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username = request.POST["username"],
            password = request.POST["password"]
        )

        if user:
            login(request, user)
            return redirect("task_list")
        else:
            error = "Invalid username or password"
            return render(request, "auth/login.html",{"error" : error})
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

############################################################

class Restaurant(models.Model):

    LOCATIONS_CHOICES = [
        ("east_london", "East London"),
        ("south_london", "South London"),
        ("north_london", "North London"),
        ("west_london", "West London")
    ]

    RESTAURANT_CUISINES = [
        ("italian", "Italian"),
        ("indian", "Indian"),
        ("british", "British"),
        ("spanish", "Spanish"),
        ("chinese", "Chinese"),
        ("japanese", "Japanese"),
        ("korean", "Korean")
    ]

    owner = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = "restaurants_owned"
    )
    restaurant_name = models.CharField(max_length = 200, null = False, blank = False)
    date_opened = models.DateField(null = False, blank = False)
    location = models.CharField( max_length = 200, choices = LOCATIONS_CHOICES)
    restaurant_cuisine = models.CharField( max_length = 200, choices = RESTAURANT_CUISINES )
    size = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.owner
    
class Staff(models.Model):

    manager = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = "employees"
        )
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name = "who_works_here"
    )

    WORK_STATUS = [
        ("temp_visa", "Temp Visa"),
        ("student_visa", "Student Visa"),
        ("eu_passport", "EU Passport"),
        ("uk_passport", "UK Passport")
    ]

    ROLES = [
        ("chief", "Chief"),
        ("waiter", "Waiter"),
        ("manager","Manager")
    ]

    name = models.CharField(max_length = 200, null = False, blank = False)
    surname = models.CharField(max_length = 200, null = False, blank = False)
    date_of_birth = models.DateField()
    age = models.IntegerField(default = date_of_birth - timezone.now)
    date_employed = models.DateTimeField(default = timezone.now)
    work_right = models.CharField(max_length = 200, choices = WORK_STATUS)
    position = models.CharField(max_length = 200, choices = ROLES, default = "waiter")

    def __str__(self):
        return f"{self.name} {self.surname}"

class MenuItem(models.Model):

    CATEGORY_CHOICES = [
        ("starter","Starter"),
        ("main","Main"),
        ("dessert","Desert"),
        ("drink","Drink"),
        ("snack","Snack"),
    ]
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name = "menu_items"
    )
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True, null = True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES, default = "main")
    availability = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant})"