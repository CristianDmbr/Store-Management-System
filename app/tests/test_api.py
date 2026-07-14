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
from django.core.exceptions import ValidationError

from rest_framework.test import APITestCase

from app.models import Restaurant, Reservation, MenuItem, Staff

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
                                "date_opened": date(2025,1,1),
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
        # Single resource doesnt have a list of dictionaries instead its a single dictionary data
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

class RestaurantSearchView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Hut",
            date_opened=date(2024, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=100
        )

        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Burger House",
            date_opened=date(2023, 1, 1),
            location="west_london",
            restaurant_cuisine="fast_food",
            capacity=80
        )

    
    def test_get_with_no_query_parameters_pass(self):
        response = self.client.get(reverse("search_api"))

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),2)
    
    def test_get_with_query_parameters_pass(self):
        response = self.client.get(reverse("search_api"), {"name" : "pizza"})

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data), 1)
        # Since we have used many = True for serializer even if there is one row, the .data is a list not just a single object.
        self.assertEqual(response.data[0]["restaurant_name"],"Pizza Hut")
    
    def test_valid_create_new_row_pass(self):
        response = self.client.post(reverse("search_api"),
                                {
                                    "owner": self.user.pk,
                                    "restaurant_name": "DGK",
                                    "date_opened": "2000-2-22",
                                    "location": "east_london",
                                    "restaurant_cuisine": "italian",
                                    "capacity": 10
                                })
        
        self.assertEqual(response.status_code,201)
        self.assertEqual(Restaurant.objects.count(),3)
        self.assertEqual(response.data["restaurant_name"],"DGK")
    
    def test_invalid_create_new_row_pass(self):
        response = self.client.post(reverse("search_api"),
                                {
                                    "restaurant_name": "DGK",
                                    "date_opened": "2000-2-22",
                                    "location": "east_london",
                                })
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(Restaurant.objects.count(),2)
    
    def test_valid_delete_pass(self):
        response = self.client.delete(reverse("search_api") + "?name=Pizza Hut")

        self.assertFalse(Restaurant.objects.filter(restaurant_name = "Pizza Hut"))
        self.assertEqual(Restaurant.objects.count(),1)
        self.assertEqual(response.status_code,204)

class ReservationListCreateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Hut",
            date_opened=date(2024, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=100
        )

        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Burger House",
            date_opened=date(2023, 1, 1),
            location="west_london",
            restaurant_cuisine="fast_food",
            capacity=80
        )
        self.reservation_1 = Reservation.objects.create(
            restaurant=self.restaurant_1,
            name_of_reservation="Mihai",
            kids=1,
            teens=2,
            adults=4,
        )

        self.reservation_2 = Reservation.objects.create(
            restaurant=self.restaurant_2,
            name_of_reservation="Alex",
            kids=0,
            teens=1,
            adults=2,
        )

        self.reservation_3 = Reservation.objects.create(
            restaurant=self.restaurant_2,
            name_of_reservation="John",
            kids=3,
            teens=0,
            adults=2,
        )
    
    def test_get_page_pass(self):
        response = self.client.get(reverse("reservations_list_create_api"))

        self.assertEqual(response.status_code,200)
        self.assertEqual(Reservation.objects.count(),3)

    def test_query_set_order_pass(self):
        response = self.client.get(reverse("reservations_list_create_api"))

        self.assertEqual(response.data[0]["name_of_reservation"], "Mihai")
        self.assertEqual(response.data[-1]["name_of_reservation"],"John")
    
    def test_post_valid_pass(self):
        response = self.client.post(reverse("reservations_list_create_api"),
                                    {
                                        "name_of_reservation" : "Marcel",
                                        "restaurant" : str(self.restaurant_1.pk),
                                        "is_active" : "True",
                                        "kids" : "2",
                                        "teens" : "1",
                                        "adults" : "9"
                                    })
        
        self.assertEqual(response.status_code,201)
        self.assertEqual(Reservation.objects.count(),4)

    def test_delete_all_posts(self):
        response = self.client.delete(reverse("reservations_list_create_api"))

        self.assertEqual(response.status_code,204)
        self.assertEqual(Reservation.objects.count(),0)
        self.assertIsNone(response.data)
    
class ReservationRetrieveUpdateDestroyAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Hut",
            date_opened=date(2024, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=100
        )

        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Burger House",
            date_opened=date(2023, 1, 1),
            location="west_london",
            restaurant_cuisine="fast_food",
            capacity=80
        )
        self.reservation_1 = Reservation.objects.create(
            restaurant=self.restaurant_1,
            name_of_reservation="Mihai",
            kids=1,
            teens=2,
            adults=4,
        )

        self.reservation_2 = Reservation.objects.create(
            restaurant=self.restaurant_2,
            name_of_reservation="Alex",
            kids=0,
            teens=1,
            adults=2,
        )

        self.reservation_3 = Reservation.objects.create(
            restaurant=self.restaurant_2,
            name_of_reservation="John",
            kids=3,
            teens=0,
            adults=2,
        )
    
    def test_get_pass_page_test(self):
        response = self.client.get(reverse("reservation_retrieve_update_destroy_api", kwargs = {"pk" : self.reservation_1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name_of_reservation"], "Mihai")
    
    def test_delete_pass(self):
        response = self.client.delete(reverse("reservation_retrieve_update_destroy_api", kwargs = {"pk" : self.reservation_1.pk}))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Reservation.objects.count(),2)
    
    def test_post_requet_pass(self):
        response = self.client.put(reverse("reservation_retrieve_update_destroy_api", kwargs = {"pk" : self.reservation_1.pk}),
                                {
                                    "name_of_reservation" : "Bob",
                                    "restaurant" : str(self.restaurant_1.pk),
                                    "is_active" : "False",
                                    "kids" : "2",
                                    "teens" : "5",
                                    "adults" : "10"
                                }
                            )
        
        self.assertEqual(response.data["name_of_reservation"], "Bob")
        self.assertEqual(response.status_code, 200)


class MenuListCreateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant_1 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Dominos",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )

        self.restaurant_2 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 30
        )

        self.menu_item_1 = MenuItem.objects.create(
            restaurant = self.restaurant_1,
            name = "Texas supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = date.today(),
            calories = 900.00,
            ingredience = "meats"
        )

        self.menu_item_2 = MenuItem.objects.create(
            restaurant = self.restaurant_1,
            name = "Vegan supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = "2022-1-2",
            calories = 900.00,
            ingredience = "meats"
        )

        self.menu_item_3 = MenuItem.objects.create(
            restaurant = self.restaurant_2,
            name = "Andys supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = "2022-1-2",
            calories = 900.00,
            ingredience = "meats"
        )
    
    def test_page_loading_200_pass(self):
        response = self.client.get(reverse("menu_list_create_api"))

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),3)
    
    def test_get_queryset_pass(self):
        response = self.client.get(reverse("menu_list_create_api"))

        self.assertEqual(response.data[0]["name"],self.menu_item_2.name)
        self.assertEqual(response.data[2]["name"],self.menu_item_3.name)
    
    def test_delete_button_pass(self):
        response = self.client.delete(reverse("menu_list_create_api"))

        self.assertEqual(response.status_code,204)
        self.assertEqual(MenuItem.objects.count(),0)
    
    def test_valid_post_pass(self):
        response = self.client.post(reverse("menu_list_create_api"),
                                    {
                                        "restaurant" : str(self.restaurant_1.pk),
                                        "name" : "fries",
                                        "description" : "French fries",
                                        "price" : "9.99",
                                        "category" : "snack",
                                        "availability" : "True",
                                        "date_added" : "2026-4-2",
                                        "calories" : "200.00",
                                        "ingredience" : "Potatoes, spice"
                                    }
                                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MenuItem.objects.count(),4)
    
class MenuItemRetrieveUpdateDestroyAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant_1 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Dominos",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )

        self.restaurant_2 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 30
        )

        self.menu_item_1 = MenuItem.objects.create(
            restaurant = self.restaurant_1,
            name = "Texas supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = date.today(),
            calories = 900.00,
            ingredience = "meats"
        )

        self.menu_item_2 = MenuItem.objects.create(
            restaurant = self.restaurant_1,
            name = "Vegan supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = "2022-1-2",
            calories = 900.00,
            ingredience = "meats"
        )

        self.menu_item_3 = MenuItem.objects.create(
            restaurant = self.restaurant_2,
            name = "Andys supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = "2022-1-2",
            calories = 900.00,
            ingredience = "meats"
        )
    
    def test_get_load_page_200(self):
        response = self.client.get(reverse("menu_item_retrieve_update_destroy_api",
                                    kwargs = {"name" : "Andys supreme", "restaurant" : "Andys"}))
    

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],"Andys supreme")
    
    def test_load_invalid_get_pass(self):
        response = self.client.get(reverse("menu_item_retrieve_update_destroy_api",
                                    kwargs = {"name" : "Bob", "restaurant" : "Bob's"}))
    
        self.assertEqual(response.status_code,404)
                                
    def test_valid_delete_pass(self):
        response = self.client.delete(reverse("menu_item_retrieve_update_destroy_api",
                                    kwargs = {"name" : "Andys supreme", "restaurant" : "Andys"}))
        
        self.assertEqual(response.status_code,204)
        self.assertIsNone(response.data)

    def test_valid_update_pass(self):
        response = self.client.put(reverse("menu_item_retrieve_update_destroy_api",
                                    kwargs = {"name" : "Andys supreme", "restaurant" : "Andys"}),
                                    {
                                        "restaurant" : str(self.restaurant_2.pk),
                                        "name" : "Updated Andys Supreme",
                                        "description" : "",
                                        "price ": "19.99",
                                        "category" : "main",
                                        "availability" : True,
                                        "date_added" : "2022-1-2",
                                        "calories" : "900.00",
                                        "ingredience" : "meats"
                                    }
                                )
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],"Updated Andys Supreme")

class StaffListCreateAPITests(APITestCase):
    
    def setUp(self):
        self.owner = User.objects.create(username = "Cristian")
    
        self.restaurant1 = Restaurant.objects.create(
            owner = self.owner,
            restaurant_name = "Dominos",
            date_opened = date.today(),
            location = "north_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )   


        self.restaurant2 = Restaurant.objects.create(
            owner = self.owner,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "north_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )  

        self.staff1 = Staff.objects.create(
            manager = self.owner,
            restaurant = self.restaurant1,
            name = "Cristian",
            surname = "Dumbravanu",
            date_of_birth = date(2003,4,22),
            date_time_employed = timezone.now(),
            work_right = "uk_passport",
            position = "manager"
        )

        self.staff2 = Staff.objects.create(
            manager = self.owner,
            restaurant = self.restaurant1,
            name = "Mihail",
            surname = "Bostan",
            date_of_birth = date(2001,1,22),
            date_time_employed = timezone.now(),
            work_right = "uk_passport",
            position = "chief"
        )

        self.staff3 = Staff.objects.create(
            manager = self.owner,
            restaurant = self.restaurant2,
            name = "Marcel",
            surname = "Cazacu",
            date_of_birth = date(2001,1,22),
            date_time_employed = timezone.now(),
            work_right = "uk_passport",
            position = "chief"   
        )
    
    def test_page_opening_pass(self):
        response = self.client.get(reverse("staff_list_create_api"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),3)
    
    def test_query_oder_pass(self):
        response = self.client.get(reverse("staff_list_create_api"))

        self.assertEqual(response.data[0]["name"],self.staff1.name)
        self.assertEqual(response.data[1]["name"],self.staff2.name)
        self.assertEqual(response.data[2]["name"],self.staff3.name)
    
    def test_create_valid_pass(self):
        response = self.client.post(reverse("staff_list_create_api"),
                                            {
                                                "manager" : str(self.owner.pk),
                                                "restaurant" : str(self.restaurant1.pk),
                                                "name" : "Jordan",
                                                "surname" : "James",
                                                "date_of_birth" : "2001-1-12",
                                                "date_time_employed" : "2026-2-10 9:00:00",
                                                "work_right" : "uk_passport",
                                                "position" : "chief",
                                                "pay_per_hour" : "10.50"
                                            })

        self.assertEqual(response.status_code,201)
        self.assertEqual(Staff.objects.count(),4)
        self.assertEqual(response.data["name"],"Jordan")
    
    def test_create_invalid_pass(self):
        response = self.client.post(reverse("staff_list_create_api"),
                                                {
                                                    "manager" : str(self.owner.pk),
                                                    "restaurant" : str(self.restaurant1.pk),
                                                    "date_of_birth" : "2001-1-12",
                                                    "date_time_employed" : "2026-2-10 9:00:00",
                                                    "work_right" : "uk_passport",
                                                    "position" : "chief",
                                                    "pay_per_hour" : "10.50"
                                                }
                                                )
        self.assertEqual(response.status_code,400)
        self.assertEqual(Staff.objects.count(),3)
    
    def test_delete_pass(self):
        response = self.client.delete(reverse("staff_list_create_api"))

        self.assertEqual(response.status_code,204)
        self.assertEqual(Staff.objects.count(),0)
    
class StaffRetrieveUpdateDestroyAPITests(APITestCase):

    def setUp(self):
            self.owner = User.objects.create(username = "Cristian")
        
            self.restaurant1 = Restaurant.objects.create(
                owner = self.owner,
                restaurant_name = "Dominos",
                date_opened = date.today(),
                location = "north_london",
                restaurant_cuisine = "fast_food",
                capacity = 25
            )   


            self.restaurant2 = Restaurant.objects.create(
                owner = self.owner,
                restaurant_name = "Andys",
                date_opened = date.today(),
                location = "north_london",
                restaurant_cuisine = "fast_food",
                capacity = 25
            )  

            self.staff1 = Staff.objects.create(
                manager = self.owner,
                restaurant = self.restaurant1,
                name = "Cristian",
                surname = "Dumbravanu",
                date_of_birth = date(2003,4,22),
                date_time_employed = timezone.now(),
                work_right = "uk_passport",
                position = "manager"
            )

            self.staff2 = Staff.objects.create(
                manager = self.owner,
                restaurant = self.restaurant1,
                name = "Mihail",
                surname = "Bostan",
                date_of_birth = date(2001,1,22),
                date_time_employed = timezone.now(),
                work_right = "uk_passport",
                position = "chief"
            )

            self.staff3 = Staff.objects.create(
                manager = self.owner,
                restaurant = self.restaurant2,
                name = "Marcel",
                surname = "Cazacu",
                date_of_birth = date(2001,1,22),
                date_time_employed = timezone.now(),
                work_right = "uk_passport",
                position = "chief",   

            )
        
    def test_valid_open_page_pass(self):
        response = self.client.get(reverse("staff_retrieve_update_destroy",
                                    kwargs = {"name" : self.staff1.name,
                                               "surname" : self.staff1.surname})
                                )
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],self.staff1.name)
        self.assertEqual(Staff.objects.count(),3)

    def test_invalid_open_page_pass(self):
        response = self.client.get(reverse("staff_retrieve_update_destroy",
                                    kwargs = {"name" : "DoesNotExist",
                                               "surname" : self.staff1.surname})
                                )
        
        self.assertEqual(response.status_code,404)
        self.assertEqual(Staff.objects.count(),3)
    
    def test_valid_put_page_pass(self):
        response = self.client.put(reverse("staff_retrieve_update_destroy",
                                    kwargs = {"name" : self.staff1.name, "surname" : self.staff1.surname}),
                                    {
                                        "manager" : str(self.owner.pk),
                                        "restaurant" : str(self.restaurant1.pk),
                                        "name" : "Cristian_updated",
                                        "surname" : "Dumbravanu_updated",
                                        "date_of_birth" : "2003-4-22",
                                        "date_time_employed" : "2025-1-1 9:00:00",
                                        "work_right" : "uk_passport",
                                        "position" : "chief",
                                        "pay_per_hour" : "10.50"
                                    }
                                    )
        
        self.staff1.refresh_from_db()
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],"Cristian_updated")
        self.assertEqual(response.data["surname"],"Dumbravanu_updated")

    def test_valid_destroy_pass(self):
        response = self.client.delete(reverse("staff_retrieve_update_destroy",
                                        kwargs = {"name" : self.staff1.name, "surname" : self.staff1.surname})
                                        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Staff.objects.count(),2)
