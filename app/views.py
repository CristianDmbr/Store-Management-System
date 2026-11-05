# Django
from django.shortcuts import get_object_or_404
from .models import Restaurant, Staff, Shift, MenuItem, Reservation, Order,OrderItem
from django.contrib.auth.models import  User
from django.middleware.csrf import get_token


# Rest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialisers import RestaurantSerializer, ReservationSerialiser, StaffSerialiser, ShiftSerialiser, MenuItemSerialiser, StaffUserCreationSerializer, StaffSupervisorSerializers, OrderSerializer, OrderItemSerializer

# Time
from datetime import timedelta
from django.utils import timezone


def calculate_restaurant_statistics(restaurant):

    today = timezone.now().date()
    last_week = today - timedelta(days = 7)
    last_month = today - timedelta(days = 31)
    last_year = today - timedelta(days = 365)

    # Finances
    total_earned_general = sum(order.total_price for order in restaurant.orders.all())
    total_earned_today = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__date = today))
    total_earned_last_week = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = last_week))
    total_earned_last_month = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = last_month))
    total_earned_last_year = sum(order.total_price for order in restaurant.orders.filter(date_time_of_order__gte = last_year))

    # Orders
    total_orders_general = len(restaurant.orders.all())
    orders_today = len(restaurant.orders.filter(date_time_of_order__date = today))
    orders_last_week = len(restaurant.orders.filter(date_time_of_order__gte = last_week))
    orders_last_month = len(restaurant.orders.filter(date_time_of_order__gte = last_month))
    orders_last_year = len(restaurant.orders.filter(date_time_of_order__gte = last_year))

    if total_earned_general > 0 and total_orders_general > 0:
        average_transaction_value = total_orders_general // total_orders_general
    else:
        average_transaction_value = 0

    # Menu
    total_menu_items = len(restaurant.menu_items.all())

    # Staff
    general_staff_count = len(restaurant.who_works_here.all())
    chief_staff_count = len(restaurant.who_works_here.filter(position = "chief"))
    waiter_staff_count = len(restaurant.who_works_here.filter(position = "waiter"))
    cleaner_staff_count = len(restaurant.who_works_here.filter(position = "cleaner"))

    if general_staff_count > 0:
        total_age = 0
        for staff in restaurant.who_works_here.all():
            total_age += staff.age
        average_age = total_age // general_staff_count
    else:
        average_age = 0

    # Labour Hours
    total_labour_hours = sum(staff.total_hours_worked for staff in restaurant.who_works_here.all())
    last_week_labour_hours = sum(staff.total_hours_worked_last_week for staff in restaurant.who_works_here.all())
    last_month_labour_hours = sum(staff.total_hours_worked_last_month for staff in restaurant.who_works_here.all())
    last_year_labour_hours = sum(staff.total_hours_worked_last_year for staff in restaurant.who_works_here.all())

    # Labour Cost
    total_labour_cost = sum(staff.total_earned for staff in restaurant.who_works_here.all())
    last_week_labour_cost = sum(staff.total_earned_this_week for staff in restaurant.who_works_here.all())
    last_month_labour_cost = sum(staff.total_earned_last_month for staff in restaurant.who_works_here.all())
    last_year_labour_cost = sum(staff.total_earned_last_year for staff in restaurant.who_works_here.all())

    # Food Stats
    all_starters = restaurant.menu_items.filter(category = "starter")
    number_of_starters = len(all_starters)
    number_of_starters_ordered = 0
    for starter in all_starters:
        for order in starter.order_items.all():
            number_of_starters_ordered += order.quantity
    
    all_mains = restaurant.menu_items.filter(category = "main")
    number_of_mains = len(all_mains)
    number_of_mains_ordered = 0
    for main in all_mains:
        for order in main.order_items.all():
            number_of_mains_ordered += order.quantity
        
    all_deserts = restaurant.menu_items.filter(category = "desert")
    number_of_deserts = len(all_deserts)
    number_of_deserts_ordered = 0
    for desert in all_deserts:
        for order in desert.order_items.all():
            number_of_deserts_ordered += order.quantity
    
    all_drinks = restaurant.menu_items.filter(category = "drink")
    number_of_drinks = len(all_drinks)
    number_of_drinks_ordered = 0
    for drink in all_drinks:
        for order in drink.order_items.all():
            number_of_drinks_ordered += order.quantity
        
    all_snacks = restaurant.menu_items.filter(category = "snack")
    number_of_snacks = len(all_snacks)
    number_of_snacks_ordered = 0
    for snack in all_snacks:
        for order in snack.order_items.all():
            number_of_snacks_ordered += order.quantity
    
    category_sales = {
        "Starter": number_of_starters_ordered,
        "Main": number_of_mains_ordered,
        "Dessert": number_of_deserts_ordered,
        "Drink": number_of_drinks_ordered,
        "Snack": number_of_snacks_ordered,
    }

    most_popular_category = max(category_sales, key = category_sales.get)

    total_number_of_items_sold = (
        number_of_starters_ordered + number_of_mains_ordered + number_of_deserts_ordered + number_of_drinks_ordered + number_of_snacks_ordered
    )

    if total_number_of_items_sold > 0:
        starters_percent = (number_of_starters_ordered / total_number_of_items_sold) * 100
        mains_percent = (number_of_mains_ordered / total_number_of_items_sold) * 100
        desserts_percent = (number_of_deserts_ordered // total_number_of_items_sold) * 100
        drinks_percent = (number_of_drinks_ordered / total_number_of_items_sold) * 100
        snacks_percent = (number_of_snacks_ordered / total_number_of_items_sold) * 100
    else:   
        starters_percent = 0
        mains_percent = 0
        desserts_percent = 0
        drinks_percent = 0
        snacks_percent = 0
    
    starter_revenue = 0
    for starter in all_starters:
        for starter_ordered in starter.order_items.all():
            starter_revenue += starter_ordered.total_cost


    main_revenue = 0
    for main in all_mains:
        for main_ordered in main.order_items.all():
            main_revenue += main_ordered.total_cost


    dessert_revenue = 0
    for dessert in all_deserts:
        for dessert_ordered in dessert.order_items.all():
            dessert_revenue += dessert_ordered.total_cost


    drink_revenue = 0
    for drink in all_drinks:
        for drink_ordered in drink.order_items.all():
            drink_revenue += drink_ordered.total_cost


    snack_revenue = 0
    for snack in all_snacks:
        for snack_ordered in snack.order_items.all():
            snack_revenue += snack_ordered.total_cost
        
    category_revenue = {
        "Starters" : starter_revenue,
        "Mains" : main_revenue,
        "Desserts" : dessert_revenue,
        "Drinks" : drink_revenue,
        "Snacks" : snack_revenue
    }

    most_profitable_category = max(category_revenue, key = category_revenue.get)
    least_profitable_category = min(category_revenue, key = category_revenue.get)

    # Reservations
    all_reservations = restaurant.reservations.all()
    reservations_for_today = restaurant.reservations.filter(reservation_date_time__date = today)
    reservations_this_week = restaurant.reservations.filter(reservation_date_time__gte = last_week)
    reservations_this_month = restaurant.reservations.filter(reservation_date_time__gte = last_month)
    reservations_this_year = restaurant.reservations.filter(reservation_date_time__gte = last_year)

    active_reservations = restaurant.reservations.filter(is_active = True)
    inactive_reservations = restaurant.reservations.filter(is_active = False)



    return {
        "restaurant" : {
            "pk" : restaurant.pk,
            "name" : restaurant.restaurant_name,
            "location" : restaurant.location,
            "cuisine" : restaurant.get_restaurant_cuisine_display(),
            "supervisor" : restaurant.supervisor.username
        },
        "financials" : {
            "total_earned_general" : total_earned_general,
            "total_earned_today" : total_earned_today,
            "total_earned_last_week" : total_earned_last_week,
            "total_earned_last_month" : total_earned_last_month,
            "total_earned_last_year" : total_earned_last_year,
            "average_transaction_value" : average_transaction_value
        },
        "orders" : {
            "total_orders_general" : total_orders_general,
            "orders_today" : orders_today,
            "orders_last_week" : orders_last_week,
            "orders_last_month" : orders_last_month,
            "orders_last_year" : orders_last_year,
        },
        "menu" : {
            "menu_size" : total_menu_items
        },
        "staff" : {
            "general_staff_count" : general_staff_count,
            "chief_staff_count" : chief_staff_count,
            "waiter_staff_count" : waiter_staff_count,
            "cleaner_staff_count" : cleaner_staff_count,
            "average_age" : average_age
        },
        "labour_hours" : {
            "total_labour_hours" : total_labour_hours,
            "last_week_labour_hours" : last_week_labour_hours,
            "last_month_labour_hours" : last_month_labour_hours,
            "last_year_labour_hours" : last_year_labour_hours,
        },
        "labour_cost" : {
            "total_labour_cost" : total_labour_cost,
            "last_week_labour_cost" : last_week_labour_cost,
            "last_month_labour_cost" : last_month_labour_cost,
            "last_year_labour_cost" : last_year_labour_cost
        },
        "food_stats" : {
            "number_of_starters_ordered" : number_of_starters_ordered,
            "number_of_starters" : number_of_starters,
            "number_of_mains_ordered" : number_of_mains_ordered,
            "number_of_mains" : number_of_mains,
            "number_of_deserts_ordered" : number_of_deserts_ordered,
            "number_of_deserts" : number_of_deserts,
            "number_of_drinks_ordered" : number_of_drinks_ordered,
            "number_of_drinks" : number_of_drinks,
            "number_of_snacks_ordered" : number_of_snacks_ordered,
            "number_of_snacks" : number_of_snacks,
            "most_popular_category" : most_popular_category,

            "starters_percent" : starters_percent,
            "mains_percent" : mains_percent,
            "desserts_percent" : desserts_percent,
            "drinks_percent" : drinks_percent,
            "snacks_percent" : snacks_percent,
        },
        "food_revenue": {
            "starter_revenue": starter_revenue,
            "main_revenue": main_revenue,
            "dessert_revenue": dessert_revenue,
            "drink_revenue": drink_revenue,
            "snack_revenue": snack_revenue,
            "most_profitable_category": most_profitable_category,
            "least_profitable_category": least_profitable_category,
        },
        "reservations": {
            "total_reservations": all_reservations.count(),
            "reservations_today": reservations_for_today.count(),
            "reservations_this_week": reservations_this_week.count(),
            "reservations_this_month": reservations_this_month.count(),
            "reservations_this_year": reservations_this_year.count(),
            "active_reservations": active_reservations.count(),
            "inactive_reservations": inactive_reservations.count(),
        }
    }

########################################################################################## Restaurant 

# Collection endpoint
class MyRestaurantsAPI(APIView):

    def get(self, request):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"detail" : "You do not have the permission to access this resource"}, 
                status = status.HTTP_403_FORBIDDEN)

        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        if is_owner:
            restaurants = Restaurant.objects.filter(owner = request.user)
            serializer = RestaurantSerializer(restaurants, many = True)
            return Response(
                {
                    "restaurants" : serializer.data,
                    "role" : "Owner"
                },
                status = status.HTTP_200_OK
            )
        elif is_supervisor:
            restaurants = Restaurant.objects.filter(supervisor = request.user)
            serializer = RestaurantSerializer(restaurants, many = True)
            return Response(
                {
                    "restaurants" : serializer.data,
                    "role" : "Supervisor"
                },
                status = status.HTTP_200_OK
            )

    def post(self, request):
        
        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"details" : "You do not have the permission to add a new Restaurant"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        serializer = RestaurantSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save(owner = request.user)

            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

# Detail Endpoint
class RestaurantDetailAPI(APIView):

    def get(self, request, restaurant_pk):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"detail" : "You do not have permission to view a Restaurant"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        if request.user.groups.filter(name = "Supervisor").exists():
            restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, supervisor = request.user)
        elif request.user.groups.filter(name = "Owner").exists():
            restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)
        elif request.user.groups.filter(name = "Staff").exists():
            restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

        serializer = RestaurantSerializer(restaurant)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )
    
    def put(self, request, restaurant_pk):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"detail" : "You do not have the permission to update a restaurant"},
                status = status.HTTP_403_FORBIDDEN
            )

        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)

        serializer = RestaurantSerializer(
            restaurant,
            data = request.data
        )

        if serializer.is_valid():
            serializer.save(owner = request.user)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    def patch(self, request, restaurant_pk):
        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"detail" : "You do not have the permission to path a row"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)

        serializer = RestaurantSerializer(
            restaurant,
            data = request.data,
            partial = True
        )

        if serializer.is_valid():
            serializer.save(owner = request.user)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, restaurant_pk):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"detail" : "You do not have the permission to delete this restaurant."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk, owner = request.user)
        restaurant.delete()

        return Response(
            {"detail" : "Restaurant deleted successfully"},
        )

class RestaurantStatsAPI(APIView):

    def get(self,request,restaurant_pk):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"detail" : "You do not have the permission to view Restaurant Stats"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)

        restaurant_stats = calculate_restaurant_statistics(restaurant)

        return Response(
            restaurant_stats,
            status = status.HTTP_200_OK
        )

########################################################################################## Staff

class MyStaffAPI(APIView):

    def get(self,request):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"detail" : "You do not have the permission to view the staff list"},
                status = status.HTTP_403_FORBIDDEN
            )

        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        if is_owner:

            all_staff = Staff.objects.filter(restaurant__owner = request.user)
            
            serializer = StaffSerialiser(all_staff, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )

        elif is_supervisor:

            all_staff = request.user.employees.all()

            serializer = StaffSerialiser(all_staff, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )

    # Even if two serializers are used we can POST using the same JSON {} but do the order of fields with the order we mention the serializers
    def post(self, request):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"detail" : "You do not have the permission to add a new employee"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        user_serializer = StaffUserCreationSerializer(
            data = request.data
        )

        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors, status = status.HTTP_400_BAD_REQUEST
            )
        
        user = user_serializer.save()

        if is_owner:

            staff_serializer = StaffSerialiser(data = request.data)

            # If the staff registation fails validation, delete the user row we created earlier
            if not staff_serializer.is_valid():
                user.delete()

                return Response(
                    staff_serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            staff = staff_serializer.save(user = user)

        elif is_supervisor:

            supervisor_staff_serializer = StaffSupervisorSerializers(data = request.data)

            if not supervisor_staff_serializer.is_valid():
                user.delete()

                return Response(
                    supervisor_staff_serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            staff = supervisor_staff_serializer.save(user = user, manager = request.user )
        
        return Response(
            StaffSerialiser(staff).data,
            status = status.HTTP_201_CREATED
        )
    
class StaffDetailAPI(APIView):

    def get(self, request, staff_pk):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
                    return Response(
                        {"detail" : "You do not have the permission to view employee"},
                        status = status.HTTP_403_FORBIDDEN
                    )
                
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        staff = get_object_or_404(Staff,pk = staff_pk)

        if is_owner:
            serializer = StaffSerialiser(staff)

            return Response(
                {"role" : "Owner",
                 "staff" : serializer.data},
                 status = status.HTTP_200_OK
            )
        elif is_supervisor:
            serializer = StaffSupervisorSerializers(staff)

            return Response(
                {"role" : "Supervisor",
                 "staff" : serializer.data},
                status = status.HTTP_200_OK
            )
    
    def delete(self, request, staff_pk):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
                    return Response(
                        {"detail" : "You do not have the permission to view employee"},
                        status = status.HTTP_403_FORBIDDEN
                    )

        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        staff = get_object_or_404(Staff, pk = staff_pk)
        user = staff.user

        staff.delete()
        user.delete()

        return Response(
            status = status.HTTP_200_OK
        )

    def put(self, request, staff_pk):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
                    return Response(
                        {"detail" : "You do not have the permission to view employee"},
                        status = status.HTTP_403_FORBIDDEN
                    )
            
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        staff = get_object_or_404(Staff, pk = staff_pk)

        if is_owner:

            serializer = StaffSerialiser(staff, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
            
        elif is_supervisor:
            serializer = StaffSupervisorSerializers(staff, data = request.data)

            if serializer.is_valid():
                staff = serializer.save(manager = request.user)
                return Response(
                    StaffSupervisorSerializers(staff).data,
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
        
    def patch(self, request, staff_pk):
        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists():
                    return Response(
                        {"detail" : "You do not have the permission to view employee"},
                        status = status.HTTP_403_FORBIDDEN
                    )
            
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()

        staff = get_object_or_404(Staff, pk = staff_pk)

        if is_owner:
            serializer = StaffSerialiser(staff, data = request.data , partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
        elif is_supervisor:
            serializer = StaffSupervisorSerializers(staff, request.data, partial = True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_200_OK
                )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

########################################################################################## Menu Items

# Could be used by both Owners and Supervisors to see the menu items for their Restaurant they own/work for
class CollectionMenuItempPerRestaurantAPI(APIView):

    def get(self,request, restaurant_pk):
        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to acess restaurant menu items"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        restaurant = get_object_or_404(Restaurant, pk = restaurant_pk)
        all_menu_items = restaurant.menu_items.all()

        restaurant_serializer = RestaurantSerializer(restaurant)
        all_menu_items_serializer = MenuItemSerialiser(all_menu_items, many = True)

        return Response(
            {"restaurant" : restaurant_serializer.data,
             "all_menu_items" : all_menu_items_serializer.data},
             status = status.HTTP_200_OK
        )

class CollectionMenuItemAPI(APIView):

    def get(self,request):

        if not request.user.groups.filter(name = "Staff").exists() and not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"detail" : "You do not have the permission to view menu items"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_owner:

            all_menu_items = MenuItem.objects.filter(restaurant__owner = request.user)

            serializer = MenuItemSerialiser(all_menu_items, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )

        elif is_supervisor:

            all_menu_items = MenuItem.objects.filter(restaurant__supervisor = request.user)

            serializer = MenuItemSerialiser(all_menu_items, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        
        elif is_staff:

            user_staff = get_object_or_404(Staff, user = request.user)
            all_menu_items = MenuItem.objects.filter(restaurant = user_staff.restaurant)

            serializer = MenuItemSerialiser(all_menu_items, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        
    def post(self, request):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"Detail" : "You do not have the permission to add a new menu item"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        serializer = MenuItemSerialiser(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    


class DetailMenuItemAPI(APIView):

    def get(self, request, menu_item_pk):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view this Menu Item"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
        serializer = MenuItemSerialiser(menu_item)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def delete(self, request, menu_item_pk):
    
        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"Detail" : "You do not have the permission to delete menu item."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_owner = request.user.groups.filter(name = "Owner").exists()

        if is_owner:

            menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
            menu_item.delete()

            return Response(
                status = status.HTTP_204_NO_CONTENT
                )
    
    def put(self, request, menu_item_pk):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"data" : "You do not have the permission to update a Menu Item"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
        serializer = MenuItemSerialiser(menu_item, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    def patch(self, request, menu_item_pk):

        if not request.user.groups.filter(name = "Owner").exists():
            return Response(
                {"data" : "You do not have the permission to patch a menu item"},
                status = status.HTTP_403_FORBIDDEN
            )    
        
        menu_item = get_object_or_404(MenuItem, pk = menu_item_pk)
        serializer = MenuItemSerialiser(menu_item, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

########################################################################################## Shifts

class CollectionShiftAPI(APIView):

    def get(self, request):

        if not request.user.groups.filter(name = "Owner").exists() and not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data": "You do not have the permission to access shift list"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_owner = request.user.groups.filter(name = "Owner").exists()
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_owner:
            all_shifts = Shift.objects.filter(employee__restaurant__owner = request.user)
            serializer = ShiftSerialiser(all_shifts, many = True)

            return Response(
                    {
                        "all_shifts" : serializer.data,
                        "role" : "Owner"
                    },
                    status = status.HTTP_200_OK
                )
        elif is_supervisor:
            all_shifts = Shift.objects.filter(employee__restaurant__supervisor = request.user)
            serializer = ShiftSerialiser(all_shifts, many = True)

            return Response(
                    {
                        "all_shifts" : serializer.data,
                        "role" : "Supervisor"
                    },
                    status = status.HTTP_200_OK
                )
        elif is_staff:
            all_shifts = Shift.objects.filter(employee__user = request.user)
            serializer = ShiftSerialiser(all_shifts, many = True)

            return Response(
                    {
                        "all_shifts" : serializer.data,
                        "role" : "Staff"
                    },
                    status = status.HTTP_200_OK
                )
    
    def post(self, request):

        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"detail" : "You do not have the permission to add a new shift"}
            )
        
        serializer = ShiftSerialiser(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
class DetailShiftAPI(APIView):

    def get(self, request, shift_pk):

        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to access a shift"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        role = "Supervisor" if request.user.groups.filter(name = "Supervisor") else "Staff"
        shift = get_object_or_404(Shift, pk = shift_pk)
        serializer = ShiftSerialiser(shift)

        return Response(
            {
                "role" : role,
                "serialized_data" : serializer.data,
                "duration_hours" : shift.duration_hours,
                "earnings" : shift.earnings
            },
            status = status.HTTP_200_OK
        )


    def delete(self, request, shift_pk):

        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to delete a shift"}
            )
        
        shift = get_object_or_404(Shift, pk = shift_pk)
        shift.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT
        )
    
    def put(self, request, shift_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to update a shift"},
                status = status.HTTP_403_FORBIDDEN
            )
    
        shift = get_object_or_404(Shift, pk = shift_pk)
        serializer = ShiftSerialiser(shift, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    def patch(self, request, shift_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission ot path a shift"},
                status = status.HTTP_400_BAD_REQUEST
            )
    
        shift = get_object_or_404(Shift, pk = shift_pk)
        serializer = ShiftSerialiser(shift, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    
########################################################################################## Reservations

class CollectionReservationAPI(APIView):

    def get(self, request):
        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view all the reservations"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()
        
        if is_supervisor:
            all_reservations = Reservation.objects.filter(restaurant__supervisor = request.user)
            serializer = ReservationSerialiser(all_reservations, many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        elif is_staff:
            
            staff_object = get_object_or_404(Staff, user = request.user)
            restaurant_pk = staff_object.restaurant.pk
            all_reservations = Reservation.objects.filter(restaurant = restaurant_pk)

            serializer = ReservationSerialiser(all_reservations,many = True)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
    
    def post(self, request):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to add a new reservation"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        serializer = ReservationSerialiser(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
class DetailReservationAPI(APIView):

    # Get, Delete, Put, Patch

    def get(self, request, reservation_pk):

        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to view a reservation."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        reservation = get_object_or_404(Reservation, pk = reservation_pk)
        serializer = ReservationSerialiser(reservation)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )
    
    def delete(self, request, reservation_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to delete a reservation"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        reservation = get_object_or_404(Reservation, pk = reservation_pk)
        reservation.delete()
        
        return Response(
            status = status.HTTP_204_NO_CONTENT
        )
    
    def put(self, request, reservation_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to update a reservation"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        reservation = get_object_or_404(Reservation, pk = reservation_pk)
        serializer = ReservationSerialiser(reservation, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    def patch(self, request, reservation_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to patch a reservation"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        reservation = get_object_or_404(Reservation, pk = reservation_pk)
        serializer = ReservationSerialiser(reservation, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
########################################################################################## Order

# Supervisors : View all orders, Add order, delete order, 
# Staff : view all orders, add order, 

class CollectionOrderAPI(APIView):

    def get(self, request):
        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view the order list."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_supervisor:

            all_orders = Order.objects.filter(restaurant__supervisor = request.user)
            serializer = OrderSerializer(all_orders, many = True)

            return Response(
                {
                    "orders" : serializer.data,
                    "role" : "supervisor"
                },
                status = status.HTTP_200_OK
            )
        elif is_staff:

            all_orders = Order.objects.filter(staff__user = request.user)
            serializer = OrderSerializer(all_orders, many = True)

            return Response(
                {
                    "orders" : serializer.data,
                    "role" : "staff"
                },
                status = status.HTTP_200_OK
            )
    def post(self, request):
        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view the order list."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_supervisor:

            serializer = OrderSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
        elif is_staff:

            serializer = OrderSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
        
class DetailOrderAPI(APIView):
    
    def get(self, request, order_pk):

        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view an Order."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()
        
        order = get_object_or_404(Order, pk = order_pk)
        if is_supervisor:
            serializer = OrderSerializer(order)
        elif is_staff:
            serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )
    
    def delete(self, request, order_pk):
        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to delete an order."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        order = get_object_or_404(Order, pk = order_pk)
        order.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT
        )
    
    def put(self, request, order_pk):

        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to update an Order"},
                status = status.HTTP_403_FORBIDDEN
            )

        order = get_object_or_404(Order, pk = order_pk)
        serializer = OrderSerializer(order, data = request.data, supervisor = request.user)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    
    def patch(self, request, order_pk):
        if not request.user.groups.filter(name = "Supervisor").exists():
            return Response(
                {"data" : "You do not have the permission to patch an Order"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        order = get_object_or_404(Order, pk = order_pk)
        serializer = OrderSerializer(order, data = request.data, supervisor = request.user, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

# Updates the order status to complete
class UpdateOrderStatusToComplete(APIView):
    
    def patch(self, request, order_pk):

        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to update the status of an order to Complete."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        order_objects = get_object_or_404(Order, pk = order_pk)

        order_objects.status = "complete"
        order_objects.save(update_fields = ["status"])

        return Response(
            {"data" : "Sucessfully updated status to Complete"},
            status = status.HTTP_200_OK
        )

class UpdateOrderStatusToWaiting(APIView):
    
    def patch(self,request,order_pk):
        
        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to update order status to waiting"},
                status = status.HTTP_403_FORBIDDEN
            )

        order_object = get_object_or_404(Order, pk = order_pk )
        order_object.status = "waiting"
        order_object.save(update_fields = ["status"])

        return Response(
            {"data" : "Sucessfully updated status to waiting"},
            status = status.HTTP_200_OK
        )


########################################################################################## Order Items

class CollectionOrderItemAPI(APIView):

    def get(self, request):

        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view an Order."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_supervisor:
            all_order_items = OrderItem.objects.filter(order__restaurant__supervisor = request.user)

            serializer = OrderItemSerializer(all_order_items, many = True, supervisor = request.user)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        elif is_staff:
            staff = get_object_or_404(Staff, user = request.user)
            restaurant = staff.restaurant
            all_order_items = OrderItem.objects.filter(order__restaurant = restaurant)
            serializer = OrderItemSerializer(all_order_items, many = True, staff = request.user)
        
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        
    def post(self, request):

        if not request.user.groups.filter(name = "Supervisor").exists() and not request.user.groups.filter(name = "Staff").exists():
            return Response(
                {"data" : "You do not have the permission to view an Order."},
                status = status.HTTP_403_FORBIDDEN
            )
        
        is_supervisor = request.user.groups.filter(name = "Supervisor").exists()
        is_staff = request.user.groups.filter(name = "Staff").exists()

        if is_supervisor:

            serializer = OrderItemSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )
        elif is_staff:

            serializer = OrderItemSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status = status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST
                )

class DetailOrderItemAPI(APIView):

    def get(self, request, order_item_pk):

        if not request.user.groups.filter(name="Supervisor").exists() and  not request.user.groups.filter(name= "Staff").exists():
            return Response(
                {"data": "You do not have permission to view this order item."},
                status=status.HTTP_403_FORBIDDEN
            )

        is_supervisor = request.user.groups.filter(name="Supervisor").exists()
        is_staff = request.user.groups.filter(name="Staff").exists()

        if is_supervisor:
            order_item = get_object_or_404(OrderItem, pk=order_item_pk )
            serializer = OrderItemSerializer( order_item, supervisor=request.user )

        elif is_staff:
            order_item = get_object_or_404(
                OrderItem,
                pk=order_item_pk,
                order__staff__user=request.user
            )
            serializer = OrderItemSerializer(
                order_item,
                staff=request.user
            )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, order_item_pk):

        if not request.user.groups.filter(name="Supervisor").exists():
            return Response(
                {"data": "You do not have permission to delete this order item."},
                status=status.HTTP_403_FORBIDDEN
            )

        order_item = get_object_or_404( OrderItem, pk=order_item_pk)

        order_item.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, order_item_pk):

        if not request.user.groups.filter(name="Supervisor").exists():
            return Response(
                {"data": "You do not have permission to update this order item."},
                status=status.HTTP_403_FORBIDDEN
            )

        order_item = get_object_or_404( OrderItem, pk=order_item_pk)

        serializer = OrderItemSerializer( order_item,data=request.data,)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, order_item_pk):

        if not request.user.groups.filter(name="Supervisor").exists():
            return Response(
                {"data": "You do not have permission to patch this order item."},
                status=status.HTTP_403_FORBIDDEN
            )

        order_item = get_object_or_404( OrderItem, pk=order_item_pk
        )

        serializer = OrderItemSerializer( order_item, data=request.data, partial=True,)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   

class OrderItemsOrderBased(APIView):

    def get(self,request, order_pk):

        if not request.user.groups.filter(name = "Supervisor") and not request.user.groups.filter(name = "Staff"):
            return Response(
                {"data" : "You do not have the permission to get all of the menu items for a order"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        all_items_ordered = OrderItem.objects.filter(order = order_pk)

        serialized = OrderItemSerializer(all_items_ordered, many = True)

        return Response(
            serialized.data,
            status = status.HTTP_200_OK
        )

class DecreaseOrderItemQuantity(APIView):

    def delete(self,request, order_item_pk):

        if not request.user.groups.filter(name = "Supervisor") and not request.user.groups.filter(name = "Staff"):
            return Response(
                {"data" : "You do not have the permission to decrease the quantity of order items"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        order_item_object = get_object_or_404(OrderItem, pk = order_item_pk)

        if order_item_object.quantity > 1 :
            order_item_object.quantity -= 1
            order_item_object.save(update_fields = ["quantity"])

            return Response(
                {
                    "message" : "Quantity decreased successfully",
                    "quantity" : order_item_object.quantity
                },
                status = status.HTTP_200_OK 
            )
        else:
            order_item_object.delete()

            return Response(
                {
                    "message" : "Order has been removed successfully",
                    "quantity" : 0
                },
                status = status.HTTP_200_OK
            )


########################################################################################## Other

# Indicates what role the user is.
class GetUserLoggedIn(APIView):

    def get(self, request):
        
        user = get_object_or_404(User, pk = request.user.pk)

        if request.user.groups.filter(name = "Owner").exists():
            role = "Owner"
        elif request.user.groups.filter(name = "Supervisor").exists():
            role = "Supervisor"
        elif request.user.groups.filter(name = "Staff").exists():
            role = "Staff"
        else:
            role = None


        return Response(
            {"username" : user.username,
             "pk" : user.pk,
             "role" : role,
             },
            status = status.HTTP_200_OK
        )
    
class CreateUserAPI(APIView):

    def post(self, request):
        serializer = StaffUserCreationSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"username" : user.username},
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    
class LoginAPI(APIView):

    def post(self, request):

        from django.contrib.auth import authenticate, login, logout

        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate asks if there credentials are valid for a user.
        # 1. Does a user with this username exist? 2. Does the password match with the stored password?
        # Yes: Return the user Object
        # No : Return None
        user = authenticate(
            request,
            username = username,
            password = password
        )

        if user is None:
            return Response(
                {"detail" : "Invalid username or password"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        
        # If the authentication passes and the user exists.
        # This means the user is not logged into this browser session.
        # Sessionid Cookies are made and Browser stores tehse cookies.
        # These cookies are used with HTTP requests 
        # < fetch("url"),{ credentials : "include"})
        login(request, user)

        if user.groups.filter(name = "Owner").exists():
            role = "Owner"
        elif user.groups.filter(name = "Supervisor").exists():
            role = "Supervisor"
        elif user.groups.filter(name = "Staff").exists():
            role = "Staff"
        else:
            role = "None"
        
        return Response(
            {
                "role" : role,
                "username" : user.username,
            },
            status = status.HTTP_200_OK
        )

from django.contrib.auth import logout
class LogoutAPI(APIView):
    def post(self,request):
        logout(request)

        return Response(
            {"detail" : "Successfully logged out"},
            status = status.HTTP_200_OK
        )
    
# Gets me the CSRF token to make sure the security mechanic works.
# Ensures the request is made from a legitimate frontend.
# Its Django that manage and sets CSRF cookie.
class GetCSRFToken(APIView):

    def get(self,request):
        return Response(
            {"csrfToken" : get_token(request)
        })
    
class GetTime(APIView):
    def get(self, request):
        curr_hour = timezone.localtime().hour
        
        if curr_hour < 12:
            greeting = "Good morning"
        elif curr_hour < 17:
            greeting = "Good afternoon"
        elif curr_hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good Night"
    
        return Response(
            {"greeting" : greeting},
            status = status.HTTP_200_OK
        )

class GetAllSupervisors(APIView):
    def get(self,request):
        supervisors = User.objects.filter(groups__name = "Supervisor")

        data = []

        for supervisor in supervisors:
            data.append(
                {
                    "id" : supervisor.pk,
                    "username" : supervisor.username
                }
            ) 
        return Response(
            data,
            status = status.HTTP_200_OK
        )
    
class GetStaffRestaurant(APIView):

    def get(self, request):

        if not request.user.groups.filter(name = "Staff").exists():
            return Response (
                {"data" : "You do not have the permission to access a staff's restaurant"},
                status.HTTP_403_FORBIDDEN
            )
        
        staff_object = get_object_or_404(Staff, user = request.user)
        restaurant_object = staff_object.restaurant

        return Response(
            {
                "restaurant_pk" : restaurant_object.pk,
                "restaurant_display_name" : restaurant_object.restaurant_name
            },
            status.HTTP_200_OK
        )
    
# Gets the Staff Object when the user is Staff.
# Used for starting orders as a Staff.
class GetStaffUser(APIView):
    def get(self,request):

        staff_object = get_object_or_404(Staff, user = request.user)

        serialized_staff_object = StaffSerialiser(staff_object)

        return Response(
            {"staff_object" : serialized_staff_object.data,
             "staff_object_pk" : staff_object.pk},
            status = status.HTTP_200_OK
        )