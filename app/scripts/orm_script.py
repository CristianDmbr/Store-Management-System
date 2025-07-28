def run():
    import random
    from datetime import timedelta, datetime
    from django.utils import timezone
    from django.contrib.contenttypes.models import ContentType

    from app.models import (
        Restaurants,
        RestaurantFinance,
        Menu,
        Inventory,
        Review,
        CostumerOrder,
        Staff,
        ShiftManager
    )

    # Clear existing data (optional)
    Restaurants.objects.all().delete()
    RestaurantFinance.objects.all().delete()
    Menu.objects.all().delete()
    Inventory.objects.all().delete()
    Review.objects.all().delete()
    CostumerOrder.objects.all().delete()
    Staff.objects.all().delete()
    ShiftManager.objects.all().delete()

    restaurant_types = [choice[0] for choice in Restaurants.RestaurantTypes.choices]
    units = [choice[0] for choice in Inventory.Units.choices]
    roles = [choice[0] for choice in Staff.Roles.choices]
    review_types = [choice[0] for choice in Review.ReviewType.choices]

    # --- Create Restaurants ---
    restaurants = []
    for i in range(5):
        r = Restaurants.objects.create(
            name=f"Resto_{i}",
            restaurant_type=random.choice(restaurant_types),
            nick_name=f"Nick_{i}",
            capacity=random.randint(20, 100),
            date_opened=timezone.now() - timedelta(days=random.randint(100, 1000))
        )
        restaurants.append(r)

    # --- Create Finance Records ---
    for r in restaurants:
        RestaurantFinance.objects.create(
            restaurant=r,
            income=random.randint(5000, 20000),
            expenditures=random.randint(1000, 15000),
            sales=random.randint(100, 1000)
        )

    # --- Create Menus ---
    menus = []
    for r in restaurants:
        for i in range(5):
            m = Menu.objects.create(
                restaurant=r,
                name=f"{r.name}_Menu_{i}",
                description="Delicious item",
                price=round(random.uniform(5.00, 30.00), 2),
                is_available=random.choice([True, False])
            )
            menus.append(m)

    # --- Create Inventory ---
    for r in restaurants:
        for i in range(3):
            Inventory.objects.create(
                restaurant=r,
                name=f"{r.name}_Stock_{i}",
                quantity=random.randint(10, 200),
                unit=random.choice(units)
            )

    # --- Create Staff ---
    staff_members = []
    for i in range(10):
        s = Staff.objects.create(
            name=f"StaffName_{i}",
            surname=f"Surname_{i}",
            date_of_birth=datetime.strptime(f"199{i}-01-01", "%Y-%m-%d").date(),
            role=random.choice(roles)
        )
        staff_members.append(s)

    # --- Create ShiftManager ---
    for staff in staff_members:
        ShiftManager.objects.create(
            staff=staff,
            start_time=timezone.now() - timedelta(hours=8),
            end_time=timezone.now()
        )

    # --- Create Orders ---
    for r in restaurants:
        for i in range(3):
            order = CostumerOrder.objects.create(
                restaurant=r,
                order_price=round(random.uniform(20.00, 100.00), 2),
                customer_name=f"Customer_{r.name}_{i}"
            )
            order.items.set(random.sample(menus, 2))

    # --- Create Reviews ---
    # Using content types to assign reviews to different models
    menu_ct = ContentType.objects.get_for_model(Menu)
    restaurant_ct = ContentType.objects.get_for_model(Restaurants)

    for i in range(10):
        target_model = random.choice([menu_ct, restaurant_ct])
        target_obj = random.choice(menus if target_model == menu_ct else restaurants)

        Review.objects.create(
            customer_name=f"Reviewer_{i}",
            comment="Nice!" if i % 2 == 0 else "Could be better.",
            review_type=random.choice(review_types),
            rating=random.randint(1, 5),
            content_type=target_model,
            object_id=target_obj.id
        )

    print("✅ Sample data created successfully!")