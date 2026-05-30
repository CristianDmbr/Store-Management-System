from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError # Returns the reason why it failed with user friendly error messages
from datetime import date, timedelta 
from django.utils import timezone

from app.models import (
    Restaurant,
    Reservation,
    Staff,
    Shift,
    MenuItem
)

from app.validators import (
    validate_unique_restaurant_name, validate_appropriate_restaurant_name,
    validate_unique_restaurant_name_reservation,
    validate_unique_name_and_surname, validate_date_employed,validate_date_of_birth,
    validate_shift_time,
    validate_unique_menu_item_name, validate_calories
)

# Test Suite for restaurant
class RestaurantValidatorTests(TestCase):

    # Test Fixure
    # This creates a real databsae row inside the temporary test database so its not just a Python variable.
    # With .create we dont run clean() or validators so we can create invalid rows. This is intentionally done to create broken rows, edgecases and impossible states. (To test different situations)
    # A Django model instance is Both a Python Object and representation of the database row. so .restaurant a Python object in memory and a real DB row.
    # So we can do both < self.restaurant.capacity > and <Restaurant.objects.filter(capacity = 50)>
    # This test DB exsists only temporarily during test runs Django Creates test DB, Run tests and then destroys the DB
    def setUp(self):
        self.user = User.objects.create(username = "admin")
    
        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Palace",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )
    
    def test_duplicate_restaurant_name_fails(self):
        # "with" just means run the code below and watch if it pass or fail
        # Besides ValidationError we can put other errors e.g. ValueError
        with self.assertRaises(ValidationError):
            validate_unique_restaurant_name("pizza palace")
        
    def test_valid_appropriate_restaurant_name(self):
        with self.assertRaises(ValidationError):
            validate_appropriate_restaurant_name("xxx")
    
class ReservationValidatorsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "admin")
    
        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Palace",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

        self.reservation = Reservation.objects.create(
            name_of_reservation = "Cristian",
            restaurant = self.restaurant,
            is_active = True,
            kids = 1,
            teens = 2,
            adults = 5
        )
    
    def test_duplicate_reservation(self):
        with self.assertRaises(ValidationError):
            # I have set restaurant to be Restaurant object not just name
            validate_unique_restaurant_name_reservation(reservation_name = "cristian", restaurant = self.restaurant)
    
class StaffValidatorsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "admin")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Palace",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

        self.staff = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant,
            name = "Cristian",
            surname = "Dumbravanu",
            date_of_birth = date(2003,4,22),
            date_employed = date(2026,1,1),
            work_right = "uk_passport",
            position = "waiter",
            pay_per_hour = 11.50
        )


    def test_unique_name_and_surname(self):
        with self.assertRaises(ValidationError):
            validate_unique_name_and_surname(name = "Cristian",surname = "Dumbravanu")
        
    def test_date_employed(self):
        future_date = timezone.now() + timedelta(days = 365)
        with self.assertRaises(ValidationError):
            validate_date_employed(future_date)
        
    # Instead of having both test under one function its more professional to have one per behaviour/scenario
    def test_date_of_birth_underage(self):
        with self.assertRaises(ValidationError):
            
            validate_date_of_birth(date(2021,4,4))
    
    def test_date_of_birth_future(self):
            with self.assertRaises(ValidationError):
                validate_date_of_birth(date(2027,4,4))
    
class ShiftValidatorTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="admin"
        )

        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Palace",
            date_opened=date.today(),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
        )

        self.staff = Staff.objects.create(
            manager=self.user,
            restaurant=self.restaurant,
            name="Cristian",
            surname="Dumbravanu",
            date_of_birth=date(2003, 4, 22),
            date_employed=timezone.now(),
            work_right="uk_passport",
            position="waiter",
            pay_per_hour=11.50
        )

        self.shift = Shift.objects.create(
            employee=self.staff,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=8),
            status="planned"
        )
    
    def test_shift_overlapping(self):
        with self.assertRaises(ValidationError):
            validate_shift_time(employee = self.staff, start_time = timezone.now(), end_time = timezone.now() + timedelta(hours = 1))
    
class ManuItemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
        username="admin")

        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Palace",
            date_opened=date.today(),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
        )
        
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Margherita Pizza",
            description="Classic pizza with tomato and mozzarella",
            price=12.99,
            category="main",
            availability=True,
            calories=850,
            ingredience="Tomato, Mozzarella, Basil"
        )
    
    def test_unique_menu_item(self):
        with self.assertRaises(ValidationError):
            validate_unique_menu_item_name(name = "Margherita Pizza",restaurant = self.restaurant)
    
    def test_calorie_count(self):
        with self.assertRaises(ValidationError):
            validate_calories(10000)