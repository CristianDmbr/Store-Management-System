from datetime import date, datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from app.models import (
    Restaurants,
    RestaurantFinance,
    Review,
    Inventory,
    Menu,
    CustomerOrder,
    Staff,
    ShiftManager,
)

def run():
    # Clear existing data (optional)
    Staff.objects.all().delete()
    ShiftManager.objects.all().delete()
    CustomerOrder.objects.all().delete()
    Menu.objects.all().delete()
    Inventory.objects.all().delete()
    Review.objects.all().delete()
    RestaurantFinance.objects.all().delete()
    Restaurants.objects.all().delete()

    # Create Restaurants
    r1 = Restaurants.objects.create(
        name="Pasta Palace",
        date_opened=date(2020, 5, 20),
        restaurant_type=Restaurants.RestaurantTypes.ITALIAN,
        nick_name="PP",
        capacity=80,
    )
    r2 = Restaurants.objects.create(
        name="Dragon Wok",
        date_opened=date(2019, 7, 15),
        restaurant_type=Restaurants.RestaurantTypes.CHINESE,
        nick_name="DW",
        capacity=100,
    )
    r3 = Restaurants.objects.create(
        name="Spice Route",
        date_opened=date(2021, 2, 10),
        restaurant_type=Restaurants.RestaurantTypes.INDIAN,
        nick_name="SR",
        capacity=60,
    )

    # Create RestaurantFinance
    RestaurantFinance.objects.create(restaurant=r1, income=120000, expenditures=90000, sales=1500)
    RestaurantFinance.objects.create(restaurant=r2, income=200000, expenditures=210000, sales=2500)
    RestaurantFinance.objects.create(restaurant=r3, income=150000, expenditures=130000, sales=1800)

    # Create Inventory items
    inv1 = Inventory.objects.create(restaurant=r1, name="Spaghetti", quantity=100, unit=Inventory.Units.KG)
    inv2 = Inventory.objects.create(restaurant=r1, name="Tomato Sauce", quantity=50, unit=Inventory.Units.LITERS)
    inv3 = Inventory.objects.create(restaurant=r2, name="Rice", quantity=200, unit=Inventory.Units.KG)
    inv4 = Inventory.objects.create(restaurant=r2, name="Soy Sauce", quantity=75, unit=Inventory.Units.LITERS)
    inv5 = Inventory.objects.create(restaurant=r3, name="Curry Powder", quantity=40, unit=Inventory.Units.PACKS)
    inv6 = Inventory.objects.create(restaurant=r3, name="Basmati Rice", quantity=120, unit=Inventory.Units.KG)

    # Create Menus
    m1 = Menu.objects.create(restaurant=r1, inventory_item=inv1, description="Classic spaghetti pasta", price=8.50, is_available=True)
    m2 = Menu.objects.create(restaurant=r1, inventory_item=inv2, description="Rich tomato sauce", price=2.50, is_available=True)
    m3 = Menu.objects.create(restaurant=r2, inventory_item=inv3, description="Steamed rice", price=3.00, is_available=True)
    m4 = Menu.objects.create(restaurant=r2, inventory_item=inv4, description="Soy sauce for dipping", price=1.50, is_available=True)
    m5 = Menu.objects.create(restaurant=r3, inventory_item=inv5, description="Spicy curry powder", price=4.00, is_available=True)
    m6 = Menu.objects.create(restaurant=r3, inventory_item=inv6, description="Basmati rice side dish", price=3.50, is_available=True)

    # Create Staff
    s1 = Staff.objects.create(name="Alice", surname="Smith", date_of_birth=date(1990, 4, 12), role=Staff.Roles.CHEF)
    s2 = Staff.objects.create(name="Bob", surname="Brown", date_of_birth=date(1985, 8, 23), role=Staff.Roles.MANAGER)
    s3 = Staff.objects.create(name="Clara", surname="Johnson", date_of_birth=date(1995, 1, 30), role=Staff.Roles.SERVER)
    s4 = Staff.objects.create(name="David", surname="Williams", date_of_birth=date(1988, 12, 5), role=Staff.Roles.HOST)

    # Create ShiftManager records
    now = datetime.now()
    ShiftManager.objects.create(staff=s1, start_time=now - timedelta(hours=8), end_time=now)
    ShiftManager.objects.create(staff=s2, start_time=now - timedelta(hours=9), end_time=now - timedelta(hours=1))
    ShiftManager.objects.create(staff=s3, start_time=now - timedelta(hours=7), end_time=now + timedelta(hours=1))
    ShiftManager.objects.create(staff=s4, start_time=now - timedelta(hours=6), end_time=now + timedelta(hours=2))

    # Create Reviews - generic foreign keys to Restaurants and Menus
    ct_restaurant = ContentType.objects.get_for_model(Restaurants)
    ct_menu = ContentType.objects.get_for_model(Menu)

    Review.objects.create(
        customer_name="Eve",
        comment="Amazing pasta, would come again!",
        review_type=Review.ReviewType.FEEDBACK,
        rating=5,
        content_type=ct_restaurant,
        object_id=r1.id,
    )
    Review.objects.create(
        customer_name="Frank",
        comment="Rice was a bit undercooked.",
        review_type=Review.ReviewType.COMPLAINT,
        rating=2,
        content_type=ct_menu,
        object_id=m3.id,
    )
    Review.objects.create(
        customer_name="Grace",
        comment="Loved the spicy curry powder!",
        review_type=Review.ReviewType.FEEDBACK,
        rating=4,
        content_type=ct_menu,
        object_id=m5.id,
    )

    # Create CustomerOrders
    order1 = CustomerOrder.objects.create(restaurant=r1, order_price=11.00, customer_name="Henry")
    order1.items.add(m1, m2)  # spaghetti + sauce

    order2 = CustomerOrder.objects.create(restaurant=r3, order_price=7.50, customer_name="Isabel")
    order2.items.add(m5, m6)  # curry powder + rice side

    order3 = CustomerOrder.objects.create(restaurant=r2, order_price=4.50, customer_name="Jack")
    order3.items.add(m3, m4)  # rice + soy sauce

    print("Sample data successfully created!")