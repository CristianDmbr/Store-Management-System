from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurants(models.Model):

    class RestaurantTypes(models.TextChoices):
        ITALIAN = 'italian', 'Italian'
        CHINESE = 'chinese', 'Chinese'
        INDIAN = 'indian', 'Indian'
        EASTER_EUROPEAN = 'eastern_european', 'Eastern European'
        FRENCH = 'french','French'
        FASTFOOD = 'fast_food', 'Fast Food'

    name = models.CharField(max_length = 20)
    date_opened = models.DateField(default = timezone.now)
    restaurant_type = models.CharField(max_length = 100,choices = RestaurantTypes.choices)
    nick_name = models.CharField(max_length = 100, blank = True)
    capacity = models.IntegerField( null = True)

    def __str__(self):
        return self.name

class RestaurantFinance(models.Model):
    restaurant = models.ForeignKey(Restaurants,on_delete = models.CASCADE)
    income = models.IntegerField()
    expenditures = models.IntegerField()
    sales = models.IntegerField()

    @property
    def is_profitable(self):
        if self.income > self.expenditures:
            revenue = self.income - self.expenditures
            print(f"Its profitable with a profit of {revenue}. ")
        else:
            loss = self.income - self.expenditures
            print(f"Its not profitable with a loss of {loss}")
    
    def __str__(self):
        return f"{self.restaurant}'s finances."


class Review(models.Model):

    class ReviewType(models.TextChoices):
        COMPLAINT = 'complaint','Complaint'
        FEEDBACK = 'feedback', 'Feedback'

    customer_name = models.CharField(max_length=100)
    comment = models.TextField(blank = True)
    review_type = models.CharField(max_length = 100, choices = ReviewType.choices, default = ReviewType.FEEDBACK)
    created_at = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(
        validators = [MinValueValidator(1),MaxValueValidator(5)]
    )

    # Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    review_target = GenericForeignKey('content_type','object_id')

    def __str__(self):
        return f"{self.customer_name} has reviewed {self.content_type} a {self.rating}/5." 

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    is_available = models.BooleanField(default = True)

class Inventory(models.Model):

    class Units(models.TextChoices):
        KG = 'kg','Kg',
        LITERES = 'L', 'L',
        PACKS = 'packs', 'Packs'

    restaurant = models.ForeignKey(Restaurants, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length = 100, choices = Units.choices)

class CostumerOrder(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete = models.CASCADE)
    items = models.ManyToManyField(Menu)
    order_price = models.DecimalField(max_digits = 8, decimal_places = 2)
    customer_name = models.CharField(max_length = 100)

class Staff(models.Model):

    class Roles(models.TextChoices):
        SERVENT = 'servent', 'Servent'
        CHIEF = 'chief', 'Chief'
        HOST = 'host', 'Host'
        MANAGEER = 'manager', 'Manager'


    name = models.CharField(max_length = 100)
    surname = models.CharField(max_length = 100)
    date_of_birth = models.DateField()
    role = models.CharField(max_length = 100, choices = Roles.choices)

class ShiftManager(models.Model):
    staff = models.ForeignKey(Staff, on_delete = models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()