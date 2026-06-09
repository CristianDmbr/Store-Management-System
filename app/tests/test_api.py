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

    def test_get_restaurant_returns_200_pass(self):
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

    def test_all_delete_button_pass(self):
        response = self.client.delete(reverse("restaurant_create_api"))

        self.assertEqual(response.status_code,204)
        self.assertEqual(Restaurant.objects.count(),0)
    
    def test_restaurant_ordered_by_date_opened_descending_order_pass(self):
        oldest_restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Old Restaurant",
            date_opened=date(2020, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
        )

        newer_restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="New Restaurant",
            date_opened=date(2022, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
        )

        response = self.client.get(reverse("restaurant_create_api"))

        self.assertEqual(response.data[0]["restaurant_name"],self.restaurant.restaurant_name)
        self.assertEqual(response.data[1]["restaurant_name"],newer_restaurant.restaurant_name)
        self.assertEqual(response.data[2]["restaurant_name"],oldest_restaurant.restaurant_name)

class RestaurantRetrieveUpdateDestroyAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")
        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )
    
    def test_get_restaurant_200_pass(self):
        response = self.client.get(reverse("restaurant_retrieve_update_destroy_api",
                                kwargs = {"pk" : self.restaurant.pk}))
        # Single resource doesnt have a list of dictionaries instead its a single dictionary
        self.assertEqual(response.status_code,200)
        self.assertEqual(Restaurant.objects.count(),1)
        self.assertEqual(response.data["restaurant_name"],self.restaurant.restaurant_name)
    
    def test_delete_restaurant_pass(self):
        response = self.client.delete(reverse("restaurant_retrieve_update_destroy_api", 
                                                kwargs = {"pk": self.restaurant.pk}))
                                            
        self.assertEqual(Restaurant.objects.count(),0)
        self.assertEqual(response.status_code, 204)
    
    def test_no_restaurant_404_pass(self):
        response = self.client.delete(reverse("restaurant_retrieve_update_destroy_api", 
                                                kwargs = {"pk": 999999}))
        
        self.assertEqual(response.status_code,404)
    
    def test_update_restaurant_pass(self):
        response = self.client.put(reverse("restaurant_retrieve_update_destroy_api",
                                            kwargs = {"pk" : self.restaurant.pk}),
                                    {
                                            "owner": self.user.pk,
                                            "restaurant_name": "Andys Updated",
                                            "date_opened": "2025-01-01",
                                            "location": "east_london",
                                            "restaurant_cuisine": "italian",
                                            "capacity": 100,
                                    })
        self.restaurant.refresh_from_db()

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["restaurant_name"],"Andys Updated")
    
    def test_invalid_put_returns_400_pass(self):
        response = self.client.put(
            reverse(
                "restaurant_retrieve_update_destroy_api",
                kwargs={"pk": self.restaurant.pk}
            ),
            {
                "restaurant_name": ""
            }
        )

        self.assertEqual(response.status_code, 400)