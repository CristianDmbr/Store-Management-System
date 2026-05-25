from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from app.models import (
    Restaurant
)

from app.validators import (
    validate_unique_restaurant_name,
    validate_appropriate_restaurant_name,
    
)