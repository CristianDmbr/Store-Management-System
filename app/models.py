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
    dateOpened = models.DateField(default = timezone.now)
    restaurantType = models.CharField(max_length = 100,choices = RestaurantTypes.choices)
    nick_name = models.CharField(max_length = 100, blank = True)
    capacity = models.IntegerField( null = True)

    def __str__(self):
        return self.name

class RestaurantFinance(models.Model):
    restaurant = models.ForeignKey(Restaurants,on_delete = models.CASCADE)
    income = models.IntegerField()
    expenditures = models.IntegerField()
    sales = models.IntegerField()

    def isProfitable(self):
        if self.income > self.expenditures:
            return 'Profitable'
        else:
            return 'Non Profitable'

class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    comment = models.TextField(blank = True)
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