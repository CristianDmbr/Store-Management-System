from django.core.exceptions import ValidationError

# Confusion about instance = None
# When we use this Validation for a CREATE we dont pass the object we want to create since its new meaning instance by default is None,
# this there is nothing for this query set array to ignore.
# If its an UPDATE request then we pass the Object itself and ignore it inside of the query set array.
def validate_unique_restaurant_name(name, instance=None):

    # Prevents infinite loop over importing validator in models.py and model in validators.py
    from .models import Restaurant

    qs = Restaurant.objects.filter(
        # __iexact means case insensitive exact match meaning pizza matches Pizza or pIzza
        restaurant_name__iexact=name
    )

    # Ignore current object during UPDATE
    if instance and instance.pk:
        qs = qs.exclude(pk=instance.pk)

    if qs.exists():
        raise ValidationError(
            f"Restaurant name '{name}' already exists."
        )

    return name 

def validate_appropriate_restaurant_name(name):

    banned_words = [
            "illegal", "banned", "fake", "spam", "scam", "virus",
            "hate", "terror", "bomb", "drugs", "xxx", "nsfw",
            "fraud", "pirate"
        ]

    if name and name.lower() in banned_words:
        raise ValidationError("This name is not appropriate.")
    
    return name

def validate_unique_restaurant_name_reservation(restaurant, reservation_name, instance = None):

    from .models import Reservation

    qs = Reservation.objects.filter(restaurant = restaurant,name_of_reservation = reservation_name)

    if instance and instance.pk:
        qs = qs.exclude(pk = instance.pk)
    if qs.exists():
        raise ValidationError(f"{reservation_name} already has an active reservation at {restaurant}.")