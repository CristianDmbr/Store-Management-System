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

from app.models import Restaurant, Reservation, MenuItem, Shift, Staff
from app.forms import RestaurantForm, ReservationForm, MenuItemForm, ShiftForm, ShiftForEmployeeForm, StaffForm

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

    def test_restaurant_list_contains_restaurants_title_pass(self):

        response = self.client.get(
            reverse("restaurant_list")
        )

        self.assertIn(self.restaurant, response.context["restaurants"])
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


class ReservationsCreateViewTests(TestCase):
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
    
    def test_loads_page_pass(self):
        response = self.client.get(reverse("create_reservation", kwargs = {"restaurant_id" : self.restaurant.pk}))

        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context["form"],ReservationForm)
        self.assertTemplateUsed(response,"create_reservation.html")
        self.assertEqual(response.context["restaurant"].restaurant_name, self.restaurant.restaurant_name)
        self.assertEqual(response.context["form"].initial["restaurant"].pk, self.restaurant.pk)
        self.assertNotIn("restaurant",response.context["form"])
    
    def test_load_invalid_restaurant_pass(self):
        response = self.client.get(reverse("create_reservation", kwargs = {"restaurant_id" : 999999}))

        self.assertEqual(response.status_code, 404)
    
    def test_create_valid_row_pass(self):
        response = self.client.post(reverse("create_reservation", kwargs = {"restaurant_id" : self.restaurant.pk}),
                                        {
                                            "restaurant" : str(self.restaurant.pk),
                                            "name_of_reservation" : "Mihai",
                                            "is_active" : "True",
                                            "kids" : "1",
                                            "teens" : "9",
                                            "adults" : "10"
                                        })

        self.assertEqual(response.status_code,302)
        self.assertEqual(Reservation.objects.count(),1)
        self.assertRedirects(response,reverse("restaurant_list"))
    
    def test_invalid_post_pass(self):
        response = self.client.post(reverse("create_reservation", kwargs = {"restaurant_id": self.restaurant.pk}),
                                    {
                                        "restaurant" : str(self.restaurant.pk),
                                        "name_of_reservation" : "",
                                    })
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(Reservation.objects.count(),0)


class MenuListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Dominos",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )

        self.menu_item = MenuItem.objects.create(
            restaurant = self.restaurant,
            name = "Texas supreme",
            description = "",
            price = 19.99,
            category = "main",
            availability = True,
            date_added = date.today(),
            calories = 900.00,
            ingredience = "meats"
        )
    
    def test_page_opening_200_pass(self):
        response = self.client.get(reverse("menu_list"))

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"menu_list.html")
        self.assertEqual(MenuItem.objects.count(),1)
        self.assertIsInstance(response.context["form"],MenuItemForm)
        
    
    def test_ordered_by_restaurant_date_added_pass(self):
        restaurant_2 = Restaurant.objects.create(
            owner=self.user,
            restaurant_name="Pizza Hut",
            date_opened=date.today(),
            location="west_london",
            restaurant_cuisine="italian",
            capacity=50
        )

        menu_item_2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Pepperoni Feast",
            description="",
            price=15.99,
            category="main",
            availability=True,
            date_added=date(2024, 1, 1),
            calories=800,
            ingredience="pepperoni"
        )

        menu_item_3 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="BBQ Chicken",
            description="",
            price=17.99,
            category="main",
            availability=True,
            date_added=date(2025, 1, 1),
            calories=850,
            ingredience="chicken"
        )

        menu_item_4 = MenuItem.objects.create(
            restaurant= restaurant_2,
            name="Veggie Delight",
            description="",
            price=13.99,
            category="main",
            availability=True,
            date_added=date(2023, 1, 1),
            calories=600,
            ingredience="vegetables"
        )

        menu_item_5 = MenuItem.objects.create(
            restaurant=restaurant_2,
            name="Meat Feast",
            description="",
            price=20.99,
            category="main",
            availability=True,
            date_added=date(2024, 6, 1),
            calories=1000,
            ingredience="mixed meats"
        )
    
        response = self.client.get(reverse("menu_list"))

        self.assertEqual(response.context["menu_items"][0],menu_item_2)
        self.assertEqual(response.context["menu_items"][4], menu_item_5)
    
    def test_valid_post_pass(self):
        response = self.client.post(reverse("menu_list"),
                                {
                                 "restaurant" : str(self.restaurant.pk),
                                 "name" : "spicy wings",
                                 "desciption" : "Spicy Wings!!",
                                 "price" : "9.99",
                                 "category" : "side",
                                 "availability" : "True",
                                 "date_added" : "2026-1-2",
                                 "calories" : "560.00"
                                }
                            )
        
        self.assertEqual(response.status_code,302)
        self.assertEqual(MenuItem.objects.count(), 2)
        self.assertRedirects(response,reverse("menu_list"))
    
    def test_invalid_post_pass(self):
        response = self.client.post(reverse("menu_list"),
                                {
                                    "restaurant" : str(self.restaurant.pk),
                                    "name" : ""
                                }
                            )
                        
        self.assertEqual(response.status_code,200)
        self.assertEqual(MenuItem.objects.count(),1)
        self.assertIsNotNone(response.context["form"].errors)

    
class StaffCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Pizza Mania",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 50
        )

        self.staff = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant,
            name = "Ana-Maria",
            surname = "Bostan",
            date_of_birth = date.today(),
            date_time_employed = timezone.now(),
            work_right = "eu_passport",
            position = "waiter",
            pay_per_hour = 10.12
        )
    
    def test_page_opening_pass(self):
        response = self.client.get(reverse("staff_view"))

        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context["form"], StaffForm)
        self.assertTemplateUsed(response,"staff_add.html")
    
    def test_valid_creation(self):
        response = self.client.post(reverse("staff_view"),
                                        {
                                            "manager" : self.user.pk,
                                            "restaurant" : self.restaurant.pk,
                                            "name" : "Mihai",
                                            "surname" : "Bos",
                                            "date_of_birth" : "2004-10-10",
                                            "date_time_employed" : "2025-10-10 09:00:00",
                                            "work_right" : "eu_passport",
                                            "position" : "waiter",
                                            "pay_per_hour" : "10.12"
                                        })
        self.assertEqual(Staff.objects.count(),2)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("staff_list"))
    
    def test_invalid_create(self):
            response = self.client.post(reverse("staff_view"),
                                        {
                                            "manager" : self.user.pk,
                                            "restaurant" : self.restaurant.pk,
                                            "date_of_birth" : "2004-10-10",
                                            "date_time_employed" : "2025-10-10 09:00:00",
                                            "work_right" : "eu_passport",
                                            "position" : "waiter",
                                            "pay_per_hour" : "10.12"
                                        })

            self.assertEqual(response.status_code,200)
            self.assertEqual(Staff.objects.count(),1)
            self.assertIsNotNone(response.context["form"].errors)
            self.assertIn("name", response.context["form"].errors)
            self.assertIn("surname", response.context["form"].errors)

class StaffListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "Cristian")

        self.restaurant1 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Andys",
            date_opened = date.today(),
            location = "east_london",
            restaurant_cuisine = "italian",
            capacity = 10
        )

        self.restaurant2 = Restaurant.objects.create(
            owner = self.user,
            restaurant_name = "Nandos",
            date_opened = date.today() - timedelta(days = 200),
            location = "east_london",
            restaurant_cuisine = "fast_food",
            capacity = 20
        )

        self.staff1 = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant1,
            name = "Cristian",
            surname = "Dumbravanu",
            date_of_birth = date(2003,4,22),
            date_time_employed = datetime.now(),
            work_right = "uk_passport",
            position = "manager"
        )

        self.staff2 = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant1,
            name = "Dumitru",
            surname = "Dumbravanu",
            date_of_birth = date(2002,6,4),
            date_time_employed = datetime.now(),
            work_right = "uk_passport",
            position = "waiter"
        )

        self.staff2 = Staff.objects.create(
            manager = self.user,
            restaurant = self.restaurant2,
            name = "Marcel",
            surname = "Dumbravanu",
            date_of_birth = date(1972,10,8),
            date_time_employed = datetime.now(),
            work_right = "eu_passport",
            position = "waiter"
        )
    
    def test_page_opening_pass(self):
        response = self.client.get(reverse("staff_list"))

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context["members_of_staff"]),3)
        self.assertEqual(Staff.objects.count(),3)
        self.assertTemplateUsed(response,"staff_list.html")
        self.assertIn("members_of_staff",response.context)

    def test_query_set_order(self):
        response = self.client.get(reverse("staff_list"))

        self.assertEqual(response.context["members_of_staff"][0],self.staff1)
        self.assertEqual(response.context["members_of_staff"][2],self.staff2)
    
    def test_empty_database_get(self):
        Staff.objects.all().delete()

        response = self.client.get(reverse("staff_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Staff.objects.count(),0)

class StaffUpdateTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create(username = "Cristian")

        self.restaurant = Restaurant.objects.create(
            owner = self.owner,
            restaurant_name = "Andy's",
            date_opened = date.today(),
            location = "south_london",
            restaurant_cuisine = "italian",
            capacity = 25
        )

        self.staff1 = Staff.objects.create(
            restaurant = self.restaurant,
            manager = self.owner,
            name = "Bob",
            surname = "Jordan",
            date_of_birth = date(2000,5,1),
            date_time_employed = timezone.now() - timedelta( hours = 10),
            work_right = "temp_visa",
            position = "waiter",
            pay_per_hour = 12.50
        )


        self.staff2 = Staff.objects.create(
            restaurant = self.restaurant,
            manager = self.owner,
            name = "Staff",
            surname = "Lewis",
            date_of_birth = date(2000,5,1),
            date_time_employed = timezone.now(),
            work_right = "student_visa",
            position = "chief",
            pay_per_hour = 10.00
        )

    def test_page_opening_pass(self):
        response = self.client.get(reverse("staff_update", 
                                        kwargs = {"pk" : self.staff1.pk}))

        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context["form"],StaffForm)
        self.assertTemplateUsed(response, "staff_update.html")
        self.assertEqual(Staff.objects.count(),2)

    def test_update_pass(self):
        response = self.client.post(
                                    reverse("staff_update",
                                    kwargs = {"pk" : self.staff1.pk}),
                                    {
                                        "manager" : str(self.owner.pk),
                                        "restaurant" : str(self.restaurant.pk),
                                        "name" : "Bob_updated",
                                        "surname" : "Dumbravanu",
                                        "date_of_birth" : "2000-5-1",
                                        "date_time_employed" : "2025-5-5 9:00:00",
                                        "work_right" : "temp_visa",
                                        "position" : "waiter",
                                        "pay_per_hour" : "20.00"
                                    }
                                    )
        
        self.assertEqual(response.status_code, 302)
        staff = Staff.objects.get(pk = self.staff1.pk)
        self.assertEqual(staff.name, "Bob_updated")
        self.assertEqual(staff.pay_per_hour, 20.00)
        self.assertRedirects(response,reverse("staff_list"))

    def test_invalid_update_pass(self):
        response = self.client.post(
                                    reverse("staff_update",
                                    kwargs = {"pk" : self.staff1.pk}),
                                    {
                                        "manager" : str(self.owner.pk),
                                        "restaurant" : str(self.restaurant.pk),
                                        # Missing Name
                                        "surname" : "Dumbravanu",
                                        "date_of_birth" : "2000-5-1",
                                        "date_time_employed" : "2025-5-5 9:00:00",
                                        "work_right" : "temp_visa",
                                        "position" : "waiter",
                                        "pay_per_hour" : "15.00"
                                    }
                                    )
                                
        staff = Staff.objects.get(pk = self.staff1.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["form"].errors)
        self.assertIn("name",response.context["form"].errors)
        self.assertEqual(staff.name, "Bob")
        

class StaffDeleteViewTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create(username = "Cristian")
    
        self.restaurant = Restaurant.objects.create(
            owner = self.owner,
            restaurant_name = "Dominos",
            date_opened = date.today(),
            location = "north_london",
            restaurant_cuisine = "fast_food",
            capacity = 25
        )   

        self.staff1 = Staff.objects.create(
            manager = self.owner,
            restaurant = self.restaurant,
            name = "Cristian",
            surname = "Dumbravanu",
            date_of_birth = date(2003,4,22),
            date_time_employed = timezone.now(),
            work_right = "uk_passport",
            position = "manager"
        )

        self.staff2 = Staff.objects.create(
            manager = self.owner,
            restaurant = self.restaurant,
            name = "Mihail",
            surname = "Bostan",
            date_of_birth = date(2001,1,22),
            date_time_employed = timezone.now(),
            work_right = "uk_passport",
            position = "chief"
        )

    def test_open_page_pass(self):
        response = self.client.get(reverse("staff_delete",
                                    kwargs = {"pk" : str(self.staff1.pk)}))
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"staff_delete.html")
        self.assertEqual(Staff.objects.count(),2)
    
    def test_valid_delete_pass(self):
        response = self.client.post(reverse("staff_delete",
                                    kwargs = {"pk" : str(self.staff1.pk)}))
        
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("staff_list"))
        self.assertEqual(Staff.objects.count(),1)
    
    def test_invalid_delete_pass(self):
        response = self.client.post(reverse("staff_delete",
                                    kwargs = {"pk" : 3}))
                                    
        self.assertEqual(response.status_code,404)
        self.assertEqual(Staff.objects.count(),2)
    
