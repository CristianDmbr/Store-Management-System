# Manually made by me
# Serialisation is converting Python objects into a format that can be sent over to the intervet (usually JSON) (Deserialization)
# This is needed because say restaurant = Restaurant.objects.first() is not understood by browser and frontend
# The serialisation doesn't convert into JSON straight away how it works is that the serialisation first takes the DJANGO objects
# and converts it into a list of Python dictionaries of that object.

# What is JSON
# A text format used to send structured data between systems.
# Example :
"""{
  "id": 1,
  "restaurant_name": "KFC",
  "capacity" : 50
}"""
# Where is JSON used:
# APIs (most important), frontend and backend communication, mobile apps, and external services
# Why JSON exists : Different systems dont understand Python objects, (It provides a universal format that can translate any language
# not just Python, that can be read by any system)

# My confusion is that at the moment I have passed a Python Object using kwargs and my templates read it all fine so why still use JSON?
# The templates and Python backend are both inside Django meaning Python Objects are allows, but separate systems like React need a universal format.

# attrs : A dictionary containing all validated serializer field values
# Used in def validate(self, attrs) when more than one field is needed and works as attrs.get("capacity")

# Because its validate_<restaurant_name> it automatically passes the restaurant name# Validation in DRF is more direct so no nead for clean_data to get data.
# Working with more than one field inside of def DRF function:
# def validate(self, attrs) attrs = attributes (Validated Python values/objects)

from rest_framework import serializers
from .models import Restaurant, Reservation, Staff, Shift, MenuItem
from .validators import  (  validate_unique_restaurant_name, validate_appropriate_restaurant_name, # Restaurant
                           validate_unique_restaurant_name_reservation, # Reservation
                           validate_unique_name_and_surname, validate_date_of_birth, validate_date_employed, # Staff
                           validate_shift_time, # Shift
                           validate_unique_menu_item_name, validate_calories # Menu Item
                           )

class RestaurantSerialiser(serializers.ModelSerializer): 
  class Meta:
    model = Restaurant
    fields = ["restaurant_name","owner","date_opened","location","restaurant_cuisine","capacity"]

  def validate(self, attrs):
    restaurant_name = attrs.get("restaurant_name")

    validate_unique_restaurant_name(restaurant_name, self.instance)
    validate_appropriate_restaurant_name(restaurant_name)

    return attrs
    
class ReservationSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Reservation
    fields = ["name_of_reservation","restaurant","is_active","kids","teens","adults"]

  def validate(self, attrs):
    name_of_reservation = attrs.get("name_of_reservation")
    restaurant = attrs.get("restaurant")

    validate_unique_restaurant_name_reservation(restaurant, name_of_reservation, self.instance)
    return attrs
    
class StaffSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Staff
    fields = ["name","surname","manager","restaurant","date_of_birth","date_employed","work_right","position","pay_per_hour"]
  
  def validate(self, attrs):

    name = attrs.get("name")
    surname = attrs.get("surname")
    date_of_birth = attrs.get("date_of_birth")
    date_employed = attrs.get("date_employed")

    validate_unique_name_and_surname(name,surname,self.instance)
    validate_date_of_birth(date_of_birth)
    validate_date_employed(date_employeed)

    return attrs
  
class ShiftSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Shift
    fields = ["employee","start_time","end_time"]

  def validate(self, attrs):
    employee = attrs.get("employee")
    start_time = attrs.get("start_time")
    end_time = attrs.get("end_time")

    validate_shift_time(employee, start_time, end_time, self.instance)
  
    return attrs
  
class MenuItemSerialiser(serializers.ModelSerializer):
  class Meta:
    model = MenuItem
    fields = ["name","restaurant","price","description","category","availability","calories","ingredience"]
  
  def validate(self, attrs):

    item_name = attrs.get("name")
    restaurant = attrs.get("restaurant")
    calories = attrs.get("calories")

    validate_unique_menu_item_name(item_name, restaurant, self.instance)
    validate_calories(calories)

    return attrs