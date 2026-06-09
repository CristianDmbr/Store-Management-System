# API tests doesn't care about templates, context, forms. Instead they care about : 
# Status code, JSON returned, database changes, serialization, correct data retrieved, ordering works, modification works, 
# (DRF API uses APITestCase from rest_framework.test for extra API helpers)

# Because DRF does not have templates we will use response.data instead of response.context. This is serialized data that gets made from model
# instance objects. (Array of python dictionaries). response.data is what gets outputed on the GET API request
#[
#  {
#    "id": 1,
#    "restaurant_name": "Pizza Place",
#    "capacity": 50
#  }
# ]

from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta

from rest_framework.test import APITestCase

from app.models import Restaurant
from app.serialisers import RestaurantSerialiser

class RestaurantListCreateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")
        # Cannot access self.restaurant["restaurant_name"] because self.restaurant is not a dictionary its an object instance.
        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

    def test_get_restaurant_returns_200(self):
        response = self.client.get(reverse("restaurant_create_api"))

        self.assertEqual(response.status_code, 200)
    
    def test_get_restaurant_contains_restaurant_pass(self):
        response = self.client.get(reverse("restaurant_create_api"))

        self.assertEqual(response.data[0]["restaurant_name"],self.restaurant.restaurant_name)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_post_create_restaurant_pass(self):
        response = self.client.post(reverse("restaurant_create_api"),
                            {
                                "owner": self.user.pk,
                                "restaurant_name": "Burger House",
                                "date_opened": "2025-01-01",
                                "location": "east_london",
                                "restaurant_cuisine": "italian",
                                "capacity": 100
                            }
                            )

        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(response.status_code, 201)

    def test_invalid_created_data_pass(self):
        response = self.client.post(reverse("restaurant_create_api"),
                                    {
                                        "restaurant_name" : " ",
                                    }
                                )
            
        self.assertEqual(response.status_code, 400),
        self.assertEqual(Restaurant.objects.count(),1)
    
    #### Add test to the cutom delete and get_query