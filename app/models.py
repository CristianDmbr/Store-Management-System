from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

# DataTimeField and DateField
# DateTime Field : date + time 2026 - 04 - 06 14:30
# DateField Field : only the date 2026 - 06 - 06
# Todays date > yesterday

# Contraints and Validation on the database level
# Database validation are rules which are enforced directly by the database meaning they cannot be bypassed, dont rely on django and
# work even outside of Django.
# Types of contraints :
# 1. Field Validation : come from model fields (name = models.CharField(null = False)) 
# 2. Custom constraints :
# class Meta:
#   constraints = [
#       models.UniqueConstraint(
#            fields=["restaurant", "name"],
#            name="unique_menu_item_per_restaurant"
#           )
#       models.CheckConstraint(
#           check=Q(end_time__gt=F("start_time")),
#           name="end_after_start"
#       )
# ]
# Things like clean() are not db level and are python only.

# Constraints VS Validation
# Constrains : rules enforced by databse itself, cannot be bypassed and always run even outside of Django (models.CheckConstraints, models.Unique)
#   Error messages are not user friendly, and have limited logic so no complex queries
# Validation : rules enforced by Django (Python code) (e.g. clean(), clean_<field> and form_is_valid())
#   Runs in Django, user friendly and can handle complex logic. THEY CAN BE BYPASSED e.g. (objects.create())
# Best Practice is to use both where Constraints is for safety net and Validation is for logic and user experience

# def clean() works in models while def clean_specifc field doesnt.
# By having validation in the model we have data protection everywhere whereas forms validation protects data inserted throught 
# forms.

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
    # Why duration and earnings are null? We calculate it at the end
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

        # Check overlapping shifts by filtering all of the shifts of the current employee where the 
        overlapping = Shift.objects.filter(
            employee=self.employee,
            # Give me all the shifts where the start time is less than end time
            start_time__lt=self.end_time,
            # Gime me all the shifts where the end time is greater than start time
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This shift overlaps with another shift for this employee")

    #########    #########    #########    #########    #########    #########    #########    #########

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time and self.employee_id:
            delta = self.end_time - self.start_time
            self.duration_hours = delta.total_seconds() / 3600

            pay = float(self.employee.pay_per_hour) if self.employee_id else 0
            self.earnings = self.duration_hours * pay

        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.employee_id} | {self.start_time} - {self.end_time}"


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