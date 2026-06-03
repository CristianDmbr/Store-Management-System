# My confusion is why have a Models test if we have a validators test and the models depend on the validators, which we already tested.
# Common things to test:
# 1. Business logic e.g. how the database/rows are stored and related. 2. Properties (@property) 3. what the __str__() returns
# 4. Constraints and model-level validation

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta

from app.models import Restaurant, Reservation, Staff, Shift, MenuItem

class RestaurantModelTests(TestCase):

    def setUp(self):
        # We create common objects needed by most test.
        # Individual test allow the creation of specific objects inside of the unit test.
        self.user = User.objects.create(username = "admin")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Place",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

    def test_str_return_restaurant_name(self):
        self.assertEqual(str(self.restaurant), "Pizza Place")


    def test_current_occupancy_returns_active_reservations_only_pass(self):

        Reservation.objects.create(
            name_of_reservation = "Bob",
            restaurant = self.restaurant,
            is_active = True,
            kids = 0,
            teens = 2,
            adults = 5
        )

        Reservation.objects.create(
            name_of_reservation = "James",
            restaurant = self.restaurant,
            is_active = True,
            kids = 2,
            teens = 5,
            adults = 9
        )

        self.assertEqual(self.restaurant.current_occupancy, 23)
    
    def test_innactive_reservation_only_pass(self):

        Reservation.objects.create(
            name_of_reservation = "Bob",
            restaurant = self.restaurant,
            is_active = False,
            kids = 1,
            teens = 5,
            adults = 12
        )

        Reservation.objects.create(
            name_of_reservation = "James",
            restaurant = self.restaurant,
            is_active = True,
            kids = 2,
            teens = 5,
            adults = 9
        )

        self.assertEqual(self.restaurant.innactive_reservations, 18)
    
    def test_reamining_spots_pass(self):
        Reservation.objects.create(
            name_of_reservation = "James",
            restaurant = self.restaurant,
            is_active = True,
            kids = 0,
            teens = 5,
            adults = 10
        )

        self.assertEqual(self.restaurant.remaining_spots, 35)
    
    def test_is_full_true(self):
        Reservation.objects.create(
            name_of_reservation = "James",
            restaurant = self.restaurant,
            is_active = True,
            kids = 5,
            teens = 20,
            adults = 25
        )

        self.assertTrue(self.restaurant.is_full, True)
    
    def test_is_full_false(self):
        Reservation.objects.create(
            name_of_reservation = "James",
            restaurant = self.restaurant,
            is_active = True,
            kids = 5,
            teens = 20,
            adults = 20 
        )

        self.assertFalse(self.restaurant.is_full, False)

class ReservationModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Place",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

        self.reservation = Reservation.objects.create(
            name_of_reservation = "Ana",
            restaurant = self.restaurant,
            is_active = True,
            kids = 4,
            teens = 10,
            adults = 20
        )
    
    def test_total_people_pass(self):
        self.assertEqual(self.reservation.total_people, 34)

class StaffModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "KFC",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 100
        )
    
        self.staff = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant,
            name = "Ana",
            surname = "Bostan",
            date_of_birth = date.today(),
            date_employed = timezone.now(),
            work_right = "uk_passport",
            position = "waiter",
            pay_per_hour = "12.00"
        )

        self.shift_1 = Shift.objects.create(
            employee=self.staff,
            start_time=timezone.now() - timedelta(hours=20),
            end_time=timezone.now() - timedelta(hours=12),
            status="completed"
        )

        self.shift_2 = Shift.objects.create(
            employee=self.staff,
            start_time=timezone.now() - timedelta(hours=10),
            end_time=timezone.now() - timedelta(hours=4),
            status="completed"
        )

        self.shift_3 = Shift.objects.create(
                employee=self.staff,
                start_time=timezone.now() - timedelta(hours=3),
                end_time=timezone.now(),
                status="completed"
        )
    
    def test_age_true(self):
        expected_age = (date.today() - self.staff.date_of_birth).days // 365

        self.assertEqual(self.staff.age, expected_age)
    
    def test_total_earned_pass(self):
        expected_total_earned = self.staff.total_earned

        self.assertEqual(expected_total_earned, 204)
    
    def test_total_hours_worked_passed(self):
        expected_total_hours_worked = self.staff.total_hours_worked

        self.assertEqual(expected_total_hours_worked, 17)

class ShiftModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "KFC",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 100
        )
    
        self.staff = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant,
            name = "Ana",
            surname = "Bostan",
            date_of_birth = date.today(),
            date_employed = timezone.now(),
            work_right = "uk_passport",
            position = "waiter",
            pay_per_hour = "12.00"
        )

        self.shift_1 = Shift.objects.create(
            employee=self.staff,
            start_time=timezone.now() - timedelta(hours=20),
            end_time=timezone.now() - timedelta(hours=12),
            status="completed"
        )

        self.shift_2 = Shift.objects.create(
            employee=self.staff,
            start_time=timezone.now() - timedelta(hours=10),
            end_time=timezone.now() - timedelta(hours=4),
            status="completed"
        )

        self.shift_3 = Shift.objects.create(
                employee=self.staff,
                start_time=timezone.now() - timedelta(hours=3),
                end_time=timezone.now(),
                status="completed"
        )
    
    def test__str__pass(self):
        
        expected = (
            f"{self.staff} | "
            f"{self.shift_1.start_time} - "
            f"{self.shift_1.end_time}" 
        )

        self.assertEqual(str(self.shift_1), expected)

class MenuItemModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create(
            username="Cristian"
        )

        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="KFC",
            date_opened=date.today(),
            location="east_london",
            restaurant_cuisine="fast_food",
            capacity=100
        )

        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Zinger Burger",
            description="Spicy chicken burger",
            price=8.99,
            category="main",
            availability=True,
            calories=650,
            ingredience="Chicken, Bun, Lettuce, Mayo"
        )
    
    def test__str__pass(self):
        excepted = (
            f"{self.menu_item.name} ({self.restaurant})"
        )