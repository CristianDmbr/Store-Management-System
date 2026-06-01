from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError # Returns the reason why it failed with user friendly error messages
from datetime import date, timedelta, datetime
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

# < python manage.py test app.tests.test_validators > 
# Checking for a result with multiple result use a () e.g. ("name","surname")


# Unit Test professional naming patter :
# < test_<condition>_<expected_result> >

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
    
    def test_restaurant_name_case_insensitive_fails(self):
        with self.assertRaises(ValidationError):
            validate_unique_restaurant_name("PIzza Palace")
    
    def test_unique_restaurant_name_pass(self):

        result = validate_unique_restaurant_name("Andys")

        self.assertEqual(result, "Andys")

    def test_duplicate_restaurant_name_fails(self):
        # "with" just means run the code below and watch if it pass or fail
        # Besides ValidationError we can put other errors e.g. ValueError
        with self.assertRaises(ValidationError):
            validate_unique_restaurant_name("pizza palace")
        
    def test_inappropriate_restaurant_name_fails(self):
        with self.assertRaises(ValidationError):
            validate_appropriate_restaurant_name("xxx")
        
    def test_appropriate_restaurant_name_pass(self):

        result = validate_appropriate_restaurant_name("Andys")

        self.assertEqual(result, "Andys")
    
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
    
    def test_unique_reservation_pass(self):

        result = validate_unique_restaurant_name_reservation(reservation_name = "Bob",restaurant = self.restaurant)

        self.assertEqual(result, "Bob" )

    def test_duplicate_reservations_fails(self):
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
            date_employed = timezone.now(),
            work_right = "uk_passport",
            position = "waiter",
            pay_per_hour = 11.50
        )

    def test_unique_name_surname_pass(self):

        result = validate_unique_name_and_surname(name = "Dumitru", surname = "Dumbravanu")

        self.assertEqual(result, ("Dumitru","Dumbravanu"))

    def test_duplicate_name_surname_fails(self):
        with self.assertRaises(ValidationError):
            validate_unique_name_and_surname(name = "Cristian",surname = "Dumbravanu")

    def test_date_employed_past_pass(self):

        past_time = timezone.make_aware(datetime(2022,2,2,22,10))

        result = validate_date_employed(past_time)

        self.assertEqual(result,past_time)    

    def test_date_employed_future_date_fails(self):
        future_date = timezone.now() + timedelta(days = 365)
        with self.assertRaises(ValidationError):
            validate_date_employed(future_date)
        
    # Instead of having both test under one function its more professional to have one per behaviour/scenario
    # It will show as a seperate dot on the terminal.

    def test_date_of_birth_pass(self):
        date_of_birth = date(2003,4,22)
        result = validate_date_of_birth(date_of_birth)

        self.assertEqual(result,date_of_birth)

    def test_date_of_birth_underage_fails(self):
        with self.assertRaises(ValidationError):
            
            validate_date_of_birth(date(2021,4,4))
    
    def test_date_of_birth_future_fails(self):
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
    
    def test_shift_pass(self):

        # If we call timezone.now() multiple times in a function it will have a slight milissecond difference so better to use variables 

        start_time = timezone.now() + timedelta(hours=20)
        end_time = timezone.now() + timedelta(hours=30)

        result = validate_shift_time(
            self.staff,
            start_time=start_time,
            end_time=end_time
        )

        self.assertEqual(
            result,
            (start_time, end_time)
        ) 

    def test_shift_overlapping_fails(self):
        with self.assertRaises(ValidationError):
            validate_shift_time(employee = self.staff, start_time = timezone.now(), end_time = timezone.now() + timedelta(hours = 1))
    
class ManuItemValidatorTests(TestCase):
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
    
    def test_unique_menu_item_pass(self):
        result = validate_unique_menu_item_name(name = "Wings", restaurant = self.restaurant)
        
        self.assertEqual(result, "Wings")
    
    def test_duplicate_menu_item_fails(self):
        with self.assertRaises(ValidationError):
            validate_unique_menu_item_name(name = "Margherita Pizza",restaurant = self.restaurant)
    
    def test_valid_calories_count_pass(self):

        result = validate_calories(100)

        self.assertEqual(result,100)

    def test_calorie_count_exceeding_fails(self):
        with self.assertRaises(ValidationError):
            validate_calories(10000)