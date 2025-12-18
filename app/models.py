from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import date


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
        return f"{self.restaurant_name} - {self.owner.username}"

    
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
    date_employed = models.DateTimeField(default = timezone.now)
    work_right = models.CharField(max_length = 200, choices = WORK_STATUS)
    position = models.CharField(max_length = 200, choices = ROLES, default = "waiter")
    pay_per_hour = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        default = 10.00
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)) 

    def __str__(self):
        return f"{self.name} {self.surname}"


class Shift(models.Model):
    employee = models.ForeignKey(
        Staff,
        on_delete = models.CASCADE,
        related_name = "shifts"
    )
    start_time = models.DateTimeField(default = timezone.now)
    end_time = models.DateTimeField()

    @property
    def duration(self):
        return self.end_time - self.start_time
    
    @property
    def duration_hours(self):
        return self.duration.total_seconds() / 3600
    
    @property
    def earnings(self):
        return self.duration_hours * float(self.employee.pay_per_hour)


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


class Ingredience(models.Model):

    UNITS = [
        ("kg","Kilograms"),
        ("mg","Miligrams"),
        ("g","Grams"),
        ("l","Liters"),
        ]

    food = models.ForeignKey(
        MenuItem,
        on_delete = models.CASCADE,
        related_name = "ingrediences"
    )
    name = models.CharField(max_length=200)
    quantity_in_stock = models.IntegerField()
    units = models.CharField(max_length = 5,choices = UNITS, null = False, blank = False)

    def __str__(self):
        return f"{self.name} Available : {self.quantity_in_stock}, Units : {self.units}"


class Recipe(models.Model):
    item = models.ForeignKey(
        MenuItem,
        on_delete = models.CASCADE,
        related_name="recipe"
    )
    ingredience = models.ManyToManyField(Ingredience)