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

from rest_framework import serializers
from .models import Restaurant

class RestaurantSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = ["restaurant_name","owner","date_opened","location","restaurant_cuisine","capacity"]