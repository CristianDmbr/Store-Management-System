from django.core.exceptions import ValidationError
from django.utils import timezone

# Confusion about instance = None
# When we use this Validation for a CREATE we dont pass the object we want to create since its new meaning instance by default is None,
# this there is nothing for this query set array to ignore.
# If its an UPDATE request then we pass the Object itself and ignore it inside of the query set array.

# Cure business rule : core rule of application lives. e.g. database validators.
# Meaning its more professional to have them inside models.py since models.py gets ran by forms, admin and so no whenerver we want to make a change.
# We do however have behavioural specific validations for forms or serialisers which do require unique validators.
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
    

def validate_unique_name_and_surname(name, surname, instance = None):

    from .models import Staff

    qs = Staff.objects.filter(name = name, surname = surname)

    if instance and instance.pk:
        qs = qs.exclude(pk = instance.pk)
    if qs.exists():
        raise ValidationError(f"{name} {surname} is already in the system.")
    
def validate_date_of_birth(dob):

    today = timezone.localdate()

    if today < dob:
        raise ValidationError(f"Date of birth cannot be in the future.")
    
    age = (today - dob).days // 365

    if age < 18:
        raise ValidationError("Employee must be at least 18 years old.")

    return dob
    
def validate_shift_time(employee, start_time,end_time, instance = None):

    if start_time and end_time:
        if end_time <= start_time:
            raise ValidationError("Incorrect shift entry. Ensure the Start Time is before the End Time.")

    from .models import Shift

    overlapping = Shift.objects.filter(
        employee = employee,
        start_time__lt = end_time,
        end_time__gt = start_time
    )

    if instance and instance.pk:
        overlapping = overlapping.exclude(pk = instance.pk)
    
    if overlapping.exists():
        raise ValidationError(f"This shift overlapps with another shift for {employee.name}  {employee.surname}.")
    
    return start_time,end_time