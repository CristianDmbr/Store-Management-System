# How view testing works:
# CBV test for : Template, Context, Form, Redirects, HTML page loads
# e.g. ListView RestaurantList : Does the page load? Does it use the correct template? Does it contain my restaurants?
# e.g. CreateView RestaurantCreate : Can I acess form, Can I create Object, Does it redirect, Do my custom modifications work?
# e.g. UpdateView RestaurantUpdate : Page returns 200, Correct form is used, Correct template is used, existing object is used, sucessfully updates
# e.g. DeleteView RestaurantDelete : returns 200, uses correct template, loads correct restaurant object, deletes retaurant, redirects, returns 302

# Also test any modifications to the parent case methods
# In Django this response we get from a self.client is a Django HttpResponse object containing 
# status_code : 200, content : rendered HTLM, context : {restaurant : <queryset>},templates : ["restaurant_list.html"]
# (API responses do not have context because there are no templates)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta 

from app.models import Restaurant
from app.forms import RestaurantForm

######################################################____Restaurant___######################################################

class RestaurantListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Place",
            date_opened=date.today(),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
        )

    def test_restaurant_list_resturns_200_pass(self):

        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_restaurant_list_uses_correct_template_pass(self):

        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertTemplateUsed(response,"restaurant_list.html")

    def test_restaurant_list_contains_restaurants_pass(self):

        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertIn(self.restaurant, response.context["restaurants"])

    def test_page_title_added_to_context_pass(self):
        
        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertEqual(response.context["page_title"],"List of all restaurant sorted by date openened.")
    
    def test_restaurant_are_ordered_by_date_opened_descending_pass(self):
        
        older_restaurant = Restaurant.objects.create(
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
            date_opened=date(2025, 1, 1),
            location="east_london",
            restaurant_cuisine="italian",
            capacity=50
            )
        
        response = self.client.get(reverse("restaurant_list"))
        restaurants = list(response.context["restaurants"])

        self.assertEqual(self.restaurant,restaurants[0])
        self.assertEqual(newer_restaurant, restaurants[1])
        self.assertEqual(older_restaurant, restaurants[2])


class RestaurantCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

    # Check if page loads
    def test_restaurant_create_returns_200_pass(self):

        response = self.client.get(reverse("restaurant_create"))

        self.assertEqual(response.status_code,200)
    
    # Check if correct form is used by checking if form instance is used.
    def test_restaurant_create_uses_restaurant_form_pass(self):

        response = self.client.get(reverse("restaurant_create"))

        self.assertIsInstance(response.context["form"],RestaurantForm)
    
    # Check if correct template is used
    def test_restaurant_create_uses_correct_template_pass(self):
        response = self.client.get(reverse("restaurant_create"))

        self.assertTemplateUsed(response, "restaurant_add.html")
    
    # Check custom prefill logic works.
    def test_restaurant_create_prefills_capacity(self):
        response = self.client.get(reverse("restaurant_create"))
        # form has an initial attribute
        self.assertEqual(response.context["form"].initial["capacity"],100)

    # Check valid POST creates restaurant row.
    # This row only exists during this single test case.
    def test_valid_post_create_restaurant_pass(self):
        response = self.client.post(
            reverse("restaurant_create"),
            {
                "owner": self.user.pk,
                "restaurant_name": "Burger House",  
                "date_opened": "2025-01-01",
                "location": "east_london",
                "restaurant_cuisine": "italian",
                "capacity": 80,
            }
        )

        self.assertEqual(Restaurant.objects.count(), 1)

    # Check redirect
    def test_valid_post_redirects_pass(self):
        response = self.client.post(
            
            reverse("restaurant_create"),
            {
                "owner": self.user.pk,
                "restaurant_name": "Burger House",
                "date_opened": "2025-01-01",
                "location": "east_london",
                "restaurant_cuisine": "italian",
                "capacity": 80,
                }
            )   
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("restaurant_list"))
    
    # Check invalid Post that does not create restaurant
    def test_invalid_post_not_create_restaurant_pass(self):
        response = self.client.post(
            reverse("restaurant_create"),
            {
                "restaurant_name" : "",
            }
        )

        self.assertEqual(Restaurant.objects.count(), 0)
        # If a post request fails it will reprint the curr page so status code is 200
        self.assertEqual(response.status_code,200)

class RestaurantUpdateViewTests(TestCase):

    def setUp(self):
        # Django model instance objects
        self.user = User.objects.create(username = "Cristian")
    
        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 100
        )

    def test_restaurant_update_load_status_200_pass(self):
        response = self.client.get(reverse("restaurant_edit",
                                    kwargs = {"pk" : self.restaurant.pk}))

        self.assertEqual(response.status_code, 200)
    
    def test_restaurant_update_correct_template_pass(self):
        response = self.client.get(reverse("restaurant_edit",
                                    kwargs = {"pk" : self.restaurant.pk}))

        self.assertTemplateUsed(response, "restaurant_update.html")
    
    def test_restaurant_update_correct_form_pass(self):

        response = self.client.get(reverse("restaurant_edit",
                                    kwargs = {"pk" : self.restaurant.pk}))

        self.assertIsInstance(response.context["form"],RestaurantForm)
    
    def test_invalid_update_does_not_change_restaurant(self):

        self.client.post(
            reverse(
                "restaurant_edit",
                kwargs={"pk": self.restaurant.pk}
            ),
            {
                "restaurant_name": ""
            }
        )

        self.restaurant.refresh_from_db()

        self.assertEqual(
            self.restaurant.restaurant_name,
            "Andys"
        )

    def test_update_form_containts_existing_restaurant_date_pass(self):
        response = self.client.get(
            reverse("restaurant_edit",
            kwargs = {"pk": self.restaurant.pk}
            )
        )
        # form.instance holds the Django model object
        self.assertEqual(response.context["form"].instance,self.restaurant)
    
    def test_update_reponse_302_pass(self):
        response = self.client.post(
            reverse("restaurant_edit",
            kwargs={"pk":self.restaurant.pk}),
            {
            "owner": self.user.pk,
            "restaurant_name": "Andys Updated",
            "date_opened": date.today(),
            "location": "east_london",
            "restaurant_cuisine": "italian",
            "capacity": 10,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("restaurant_list"))
    
    def test_valid_post_updates_restaurant_pass(self):
        self.client.post(
            reverse("restaurant_edit",kwargs={"pk" : self.restaurant.pk}),
            {
                "owner": self.user.pk,
                "restaurant_name": "Andys Updated",
                "date_opened": date.today(),
                "location": "east_london",
                "restaurant_cuisine": "italian",
                "capacity": 10,
            }
        )

        self.restaurant.refresh_from_db()

        self.assertEqual(self.restaurant.restaurant_name,"Andys Updated")
        self.assertEqual(self.restaurant.capacity,10)

class RestaurantDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "west_london",
            restaurant_cuisine = "fast_food",
            capacity = "200"
        )

    def test_restaurant_delete_status_code_200_pass(self):
        response = self.client.get(reverse("restaurant_delete",
                                    kwargs={"pk":self.restaurant.pk}))

        self.assertEqual(response.status_code,200)

    def test_restaurant_delete_correct_template_used_pass(self):
        response = self.client.get(reverse("restaurant_delete",
                                    kwargs={"pk":self.restaurant.pk}))

        self.assertTemplateUsed(response, "restaurant_delete.html")
    
    def test_restaurant_delete_correct_get_objects_pass(self):
        response = self.client.get(reverse("restaurant_delete",
                                    kwargs={"pk":self.restaurant.pk}))
        
        self.assertEqual(response.context["object"], self.restaurant)
    
    def test_restaurant_detele_check_deletes_restaurant_pass(self):
        response = self.client.post(reverse("restaurant_delete",
                                    kwargs={"pk" : self.restaurant.pk}))
        
        self.assertEqual(Restaurant.objects.count(),0)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("restaurant_list"))

