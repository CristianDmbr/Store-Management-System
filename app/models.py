from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError


class Restaurant(models.Model):

    LOCATIONS_CHOICES = [
        ("east_london", "East London"),
        ("south_london", "South Lo ndon"),
        ("north_london", "North London"),
        ("west_london", "West London") 
    ]

    RESTAURANT_CUISINES = [
        ("fast_food","Fast Food"),
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
    capacity = models.IntegerField()

    # How does self.reservations works? Because we made a Foreing key inside of the Reservation class to the Restaurant,
    # we automatically have a manager tool / query interface as self.reservation_set (by default). We renamed the reversed relationship
    # in the reservation to reservation from reservation_set. 
    @property
    def current_occupancy(self):
        return sum(
            r.number_of_people for r in self.reservations.filter(is_active = True)
        )
    
    @property
    def remaining_spots(self):
        return self.capacity - self.current_occupancy
    
    @property
    def is_full(self):
        return self.current_occupancy >= self.capacity

    def __str__(self):
        return f"{self.restaurant_name}"
    
class Reservation(models.Model):
    name_of_reservation = models.CharField(max_length=200, null = False, blank = False)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "reservations")
    number_of_people = models.IntegerField()
    is_active = models.BooleanField(default = True)

    
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
        return (today - self.date_of_birth).days // 365

    def __str__(self):
        return f"{self.name} {self.surname}"


class Shift(models.Model):
    employee = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="shifts"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("active", "Active"),
        ("completed", "Completed")
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    # def clean is also recognised inside of the models and is used in the background when form validation is calling all
    # field validation.
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")

        # Check overlapping shifts
        overlapping = Shift.objects.filter(
            employee=self.employee,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This shift overlaps with another shift for this employee")

    def save(self, *args, **kwargs):
        # Calculate duration and earnings automatically
        delta = self.end_time - self.start_time
        self.duration_hours = delta.total_seconds() / 3600
        self.earnings = self.duration_hours * float(self.employee.pay_per_hour)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} | {self.start_time} - {self.end_time}"


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

    name = models.CharField(max_length = 200, blank = False, null = False)
    description = models.TextField(blank=True, null = True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES, default = "main")
    availability = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    calories = models.DecimalField(
        max_digits = 6,
        decimal_places = 2
    )
    ingredience = models.TextField(blank= True, null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["restaurant","name"],
                name = "unique_menu_item_per_restaurant"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.restaurant})"