from app.models import Restaurants, Review, RestaurantFinance
from django.contrib.contenttypes.models import ContentType

def run():
    example = RestaurantFinance.objects.first()
    print(example)