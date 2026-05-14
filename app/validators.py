from django.core.exceptions import ValidationError
from .models import Restaurant

def validate_unique_restaurant_name(name, instance=None):

    qs = Restaurant.objects.filter(
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