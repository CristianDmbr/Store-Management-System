from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Restaurant
from django.core.exceptions import ValidationError # Returns the reason why it failed with user friendly error messages
from datetime import date, timedelta

from app.models import (
    Restaurant
)

from app.validators import (
    validate_unique_restaurant_name,
    validate_appropriate_restaurant_name,
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
        with self.assertRaises(ValidationError):
            validate_unique_restaurant_name("pizza palace")