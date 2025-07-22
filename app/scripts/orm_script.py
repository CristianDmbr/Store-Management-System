from app.models import Restaurants, Review, RestaurantFinance
from django.contrib.contenttypes.models import ContentType

def run():
    restaurantExample = Restaurants.objects.first()

    restaurantFinanceCreated = RestaurantFinance.objects.create(
        restaurant = restaurantExample,
        income = 10000,
        expenditures = 100,
        sales = 60
    )

    restaurantFinanceCreated.is_profitable