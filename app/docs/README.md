# **Restaurant Management System**

## Project Overview : 
  - This is a Restaurant Management system that can be used by both Restaurant Business owners, Supervisors / Managers or regular memebers of staff to operate a business and have a centralised application that handles every aspect of a running a restaurant business.
  - The general problem is solves is simplifies the management and operation of a Restaurant by having every information and aspect of a Restaurant be ran through / managed thgouth this app. These operations inlcude from general system hiring of new staff, managing Restaurans, managing order and menu items to shift management and employee information.
  - The intended users include Owners, Supervisors / Managers and regular members of staff. Every role has its own functionality and permission to make on e.g. Orders, Shifts, Restaurant Information or Staff management.
  - What makes it useful is that instead of utilising different platforms to have manage different aspects and have problems with them having synchronised information, this application is centralised and the information stored is shared and updated between every part of the functionality.
---

## screenshots :
### 1. Authentication & Dashboards
![Login Page](app/docs/screenshots/login.png)
![Owner Dashboard](app/docs/screenshots/owner_dashboard.png)
![Supervisor Dashboard](app/docs/screenshots/supervisor_dashboard.png)
![Staff Dashboard](app/docs/screenshots/staff_dashboard.png)

### 2. Owner Functionality
The owner can manage restaurants and oversee their operations.
![Restaurant List](app/docs/screenshots/owner_restaurant_list.png)
![Restaurant Information](app/docs/screenshots/restaurant_stat_1.png)
![Restaurant Information](app/docs/screenshots/restaurant_stat_2.png)
![Restaurant Information](app/docs/screenshots/restaurant_stat_3.png)
![Add Staff](app/docs/screenshots/add_staff.png)

### 3. Supervisor Functionality
Supervisors can manage restaurant staff and coordinate employee shifts.
![Staff List](app/docs/screenshots/staff_list.png)
![Shift Management](app/docs/screenshots/shift_list_supervisor.png)
![Add Shift](app/docs/screenshots/add_shift.png)

### 4. Staff Functionality
Staff members can view menus, manage orders and access their shift information.
![Menu List](app/docs/screenshots/menu_list_staff.png)
![Menu Item Information](app/docs/screenshots/menu_item_info.png)
![Orders List](app/docs/screenshots/order_list.png)
![Start Order](app/docs/screenshots/start_order.png)
![Shift List](app/docs/screenshots/shift_list.png)
![Shift Information](app/docs/screenshots/shift_info.png)

---

## Key Features :
- User authentication and session management.
- Role Based access control and role specific perfmissions and functionality.

---

# Database Design :
- Covered Restaurant aspects : 
  - Restaurant -> (Supervisor, cuisine type, restaurant name, date opened, location, capacity and number of tables)
  - Reservations -> (At which restaurant, number of kids, teens or adults, contact number)
  - Staff -> (User's account linked, manager, restaurant, work status, position / role, personal information, pay per hour) 
  - Shift -> (Status, start / end time, duration)
  - Menu Items -> (Category, name, description, price, availability, calories and ingrediences)
  - Order -> (Status, staff who served, reservation, table number, any notes)
  - Ordered Items -> (Link to the order, menu item, quantity, price sold at)

---

## Technology Stack :

- Frontend : React, JavaScript, HTML, JSX
- Frontend Tooling : Vite
- Routing : React Router
  
- Backend : Python, Django
- API : Django REST Framework
- Database : SQLite 3
- Version / Backupds : GitHub
---

## Restaurant EndPoints

### 1. Restaurant Collection

`api/my_restaurants/`

**Description:** Collection endpoint for retrieving and creating
Restaurant objects.

**GET:** - **Permissions:** Owner and Supervisor. - **Owner:** Returns
restaurants owned by the authenticated user. - **Supervisor:** Returns
restaurants managed by the authenticated user. - **Response:**
Collection of restaurants and the user's role. - **Serializer:**
`RestaurantSerializer`

**POST:** - **Permissions:** Owner only. - **Behaviour:** Creates a
restaurant and assigns `request.user` as its owner. - **Response:**
Newly created Restaurant object. - **Serializer:**
`RestaurantSerializer`

------------------------------------------------------------------------

### 2. Restaurant Detail

`api/detail_restaurant/<int:restaurant_pk>`

**Description:** Retrieves, updates or deletes a specific Restaurant.
Requires `restaurant_pk`.

**GET:** - **Permissions:** Owner, Supervisor or Staff. - **Behaviour:**
Retrieves the specified Restaurant according to the user's role. -
**Response:** Restaurant object. - **Serializer:**
`RestaurantSerializer`

**PUT:** - **Permissions:** Owner only. - **Behaviour:** Fully updates
the Restaurant using submitted data. - **Response:** Updated Restaurant
object. - **Serializer:** `RestaurantSerializer`

**PATCH:** - **Permissions:** Owner only. - **Behaviour:** Partially
updates the Restaurant. - **Response:** Updated Restaurant object. -
**Serializer:** `RestaurantSerializer`

**DELETE:** - **Permissions:** Owner only. - **Behaviour:** Deletes the
Restaurant. - **Response:** Successful HTTP response.

------------------------------------------------------------------------

### 3. Restaurant Statistics

`api/restaurant_stats/<int:restaurant_pk>`

**Description:** Retrieves statistics for a Restaurant using
`calculate_restaurant_statistics()`. Requires `restaurant_pk`.

**GET:** - **Permissions:** Owner only. - **Behaviour:** Calculates
statistics using the specified Restaurant's data. - **Response:** Nested
dictionary containing restaurant statistics.

**Example Response Structure:**

``` json
{
    "financials": {
        "total_earned_today": "...",
        "total_earned_general": "...",
        "average_transaction_value": "..."
    },
    "orders": {
        "total_orders_general": "...",
        "orders_today": "..."
    },
    "menu": {},
    "staff": {},
    "reservations": {}
}
```

------------------------------------------------------------------------

## Staff EndPoints

### 1. Staff Collection

`api/all_staff`

**Description:** Collection endpoint for retrieving and creating Staff
objects.

**GET:** - **Permissions:** Owner and Supervisor. - **Owner:** Returns
staff employed at restaurants owned by the authenticated user. -
**Supervisor:** Returns employees managed by the authenticated user. -
**Response:** Collection of Staff objects. - **Serializer:**
`StaffSerialiser`

**POST:** - **Permissions:** Owner and Supervisor. - **Owner:** Creates
a User account and associated Staff object using `StaffSerialiser`. -
**Supervisor:** Creates a User account and associated Staff object using
`StaffSupervisorSerializers`; assigns the authenticated Supervisor as
manager. - **Behaviour:** Deletes the newly created User if Staff
serializer validation fails. - **Response:** Newly created Staff
object. - **Serializers:** `StaffUserCreationSerializer`,
`StaffSerialiser`, `StaffSupervisorSerializers` - **Status Codes:**
`201 Created` on success; `400 Bad Request` on validation failure.

------------------------------------------------------------------------

### 2. Staff Detail

`api/detail_staff/<int:staff_pk>`

**Description:** Retrieves, updates or deletes a specific Staff object.
Requires `staff_pk`.

**GET:** - **Permissions:** Owner and Supervisor. - **Owner:** Retrieves
Staff using `StaffSerialiser`. - **Supervisor:** Retrieves Staff using
`StaffSupervisorSerializers`. - **Response:** Staff object alongside the
authenticated user's role. - **Serializers:** `StaffSerialiser`,
`StaffSupervisorSerializers`

**PUT:** - **Permissions:** Owner and Supervisor. - **Behaviour:** Fully
updates Staff. Owner uses `StaffSerialiser`; Supervisor uses
`StaffSupervisorSerializers` and is assigned as manager. - **Response:**
Updated Staff object. - **Serializers:** `StaffSerialiser`,
`StaffSupervisorSerializers`

**PATCH:** - **Permissions:** Owner and Supervisor. - **Behaviour:**
Partially updates Staff using the role-appropriate serializer. -
**Response:** Updated Staff object. - **Serializers:**
`StaffSerialiser`, `StaffSupervisorSerializers`

**DELETE:** - **Permissions:** Owner and Supervisor. - **Behaviour:**
Deletes the Staff object and its associated User account. -
**Response:** Successful HTTP response.

------------------------------------------------------------------------

## Menu Item EndPoints

### 1. Menu Items Per Restaurant

`api/menu_items_per_restaurants/<int:restaurant_pk>`

**Description:** Retrieves all MenuItem objects associated with a
specific Restaurant. Requires `restaurant_pk`.

**GET:** - **Permissions:** Owner, Supervisor and Staff. -
**Behaviour:** Retrieves the Restaurant and its associated menu items. -
**Response:** Nested Restaurant and MenuItem data. - **Serializers:**
`RestaurantSerializer`, `MenuItemSerialiser`

------------------------------------------------------------------------

### 2. Menu Item Collection

`api/menu_items_list`

**Description:** Collection endpoint for retrieving and creating
MenuItem objects.

**GET:** - **Permissions:** Owner, Supervisor and Staff. - **Owner:**
Retrieves menu items belonging to restaurants owned by the authenticated
user. - **Supervisor:** Retrieves menu items belonging to restaurants
managed by the authenticated user. - **Staff:** Retrieves menu items
belonging to the Staff member's restaurant. - **Response:** Collection
of MenuItem objects. - **Serializer:** `MenuItemSerialiser`

**POST:** - **Permissions:** Owner only. - **Behaviour:** Creates a
MenuItem using submitted request data. - **Response:** Newly created
MenuItem object. - **Serializer:** `MenuItemSerialiser`

------------------------------------------------------------------------

### 3. Menu Item Detail

`api/menu_item_detail/<int:menu_item_pk>`

**Description:** Retrieves, updates or deletes a specific MenuItem.
Requires `menu_item_pk`.

**GET:** - **Permissions:** Owner, Supervisor and Staff. -
**Behaviour:** Retrieves the specified MenuItem. - **Response:**
MenuItem object. - **Serializer:** `MenuItemSerialiser`

**PUT:** - **Permissions:** Owner only. - **Behaviour:** Fully updates
the MenuItem. - **Response:** Updated MenuItem object. - **Serializer:**
`MenuItemSerialiser`

**PATCH:** - **Permissions:** Owner only. - **Behaviour:** Partially
updates the MenuItem. - **Response:** Updated MenuItem object. -
**Serializer:** `MenuItemSerialiser`

**DELETE:** - **Permissions:** Owner only. - **Behaviour:** Deletes the
MenuItem. - **Response:** `204 No Content`.

------------------------------------------------------------------------

## Shift EndPoints

### 1. Shift Collection

`api/shift_list`

**Description:** Collection endpoint for retrieving and creating Shift
objects.

**GET:** - **Permissions:** Owner, Supervisor and Staff. - **Owner:**
Retrieves shifts belonging to employees at restaurants owned by the
authenticated user. - **Supervisor:** Retrieves shifts belonging to
employees at restaurants managed by the authenticated user. - **Staff:**
Retrieves shifts assigned to the authenticated Staff user. -
**Response:** Collection of Shift objects alongside the user's role. -
**Serializer:** `ShiftSerialiser`

**POST:** - **Permissions:** Supervisor only. - **Behaviour:** Creates a
Shift using submitted request data. - **Response:** Newly created Shift
object. - **Serializer:** `ShiftSerialiser` - **Status Code:** `200 OK`
in the current implementation.

------------------------------------------------------------------------

### 2. Shift Detail

`api/shift_detail/<int:shift_pk>`

**Description:** Retrieves, updates or deletes a specific Shift.
Requires `shift_pk`.

**GET:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Retrieves the Shift and calculates additional information. -
**Response:** User role, serialized Shift, shift duration in hours and
shift earnings. - **Serializer:** `ShiftSerialiser`

**PUT:** - **Permissions:** Supervisor only. - **Behaviour:** Fully
updates the Shift using submitted data. - **Response:** Updated Shift
object. - **Serializer:** `ShiftSerialiser`

**PATCH:** - **Permissions:** Supervisor only. - **Behaviour:**
Partially updates the Shift. - **Response:** Updated Shift object. -
**Serializer:** `ShiftSerialiser`

**DELETE:** - **Permissions:** Supervisor only. - **Behaviour:** Deletes
the Shift. - **Response:** `204 No Content`.

------------------------------------------------------------------------

## Reservation EndPoints

### 1. Reservation Collection

`api/reservation_list`

**Description:** Collection endpoint for retrieving and creating
Reservation objects.

**GET:** - **Permissions:** Supervisor and Staff. - **Supervisor:**
Retrieves reservations belonging to restaurants managed by the
authenticated user. - **Staff:** Retrieves reservations belonging to the
Staff member's restaurant. - **Response:** Collection of Reservation
objects. - **Serializer:** `ReservationSerialiser`

**POST:** - **Permissions:** Supervisor only. - **Behaviour:** Creates a
Reservation using submitted request data. - **Response:** Newly created
Reservation object. - **Serializer:** `ReservationSerialiser` - **Status
Codes:** `201 Created` on success; `400 Bad Request` on validation
failure.

------------------------------------------------------------------------

### 2. Reservation Detail

`api/detail_reservation/<int:reservation_pk>`

**Description:** Retrieves, updates or deletes a specific Reservation.
Requires `reservation_pk`.

**GET:** - **Permissions:** Supervisor only. - **Behaviour:** Retrieves
the specified Reservation. - **Response:** Reservation object. -
**Serializer:** `ReservationSerialiser`

**PUT:** - **Permissions:** Supervisor only. - **Behaviour:** Fully
updates the Reservation. - **Response:** Updated Reservation object. -
**Serializer:** `ReservationSerialiser`

**PATCH:** - **Permissions:** Supervisor only. - **Behaviour:**
Partially updates the Reservation. - **Response:** Updated Reservation
object. - **Serializer:** `ReservationSerialiser`

**DELETE:** - **Permissions:** Supervisor only. - **Behaviour:** Deletes
the Reservation. - **Response:** `204 No Content`.

------------------------------------------------------------------------

## Order EndPoints

### 1. Order Collection

`api/order_list`

**Description:** Collection endpoint for retrieving and creating Order
objects.

**GET:** - **Permissions:** Supervisor and Staff. - **Supervisor:**
Retrieves orders belonging to restaurants managed by the authenticated
user. - **Staff:** Retrieves orders associated with the authenticated
Staff account. - **Response:** Collection of Order objects alongside the
user's role. - **Serializer:** `OrderSerializer`

**POST:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Creates an Order using submitted request data. - **Response:** Newly
created Order object. - **Serializer:** `OrderSerializer` - **Status
Codes:** `201 Created` on success; `400 Bad Request` on validation
failure.

------------------------------------------------------------------------

### 2. Order Detail

`api/detail_order/<int:order_pk>`

**Description:** Retrieves, updates or deletes a specific Order.
Requires `order_pk`.

**GET:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Retrieves the specified Order. - **Response:** Order object. -
**Serializer:** `OrderSerializer`

**PUT:** - **Permissions:** Supervisor only. - **Behaviour:** Fully
updates the Order; the authenticated Supervisor is passed to the
serializer. - **Response:** Updated Order object. - **Serializer:**
`OrderSerializer`

**PATCH:** - **Permissions:** Supervisor only. - **Behaviour:**
Partially updates the Order; the authenticated Supervisor is passed to
the serializer. - **Response:** Updated Order object. - **Serializer:**
`OrderSerializer`

**DELETE:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Deletes the Order. - **Response:** `204 No Content`.

------------------------------------------------------------------------

### 3. Update Order Status to Complete

`api/order_update_to_complete/<int:order_pk>`

**Description:** Action endpoint for changing an Order's status to
`complete`. Requires `order_pk`.

**PATCH:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Sets the Order status to `complete` and saves the change. -
**Response:** Confirmation message.

**Example Response:**

``` json
{
    "data": "Sucessfully updated status to Complete"
}
```

------------------------------------------------------------------------

### 4. Update Order Status to Waiting

`api/order_update_to_waiting/<int:order_pk>`

**Description:** Action endpoint for changing an Order's status to
`waiting`. Requires `order_pk`.

**PATCH:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Sets the Order status to `waiting` and saves the change. - **Response:**
Confirmation message.

**Example Response:**

``` json
{
    "data": "Sucessfully updated status to waiting"
}
```

------------------------------------------------------------------------

## Order Item EndPoints

### 1. Order Item Collection

`api/order_item`

**Description:** Collection endpoint for retrieving and creating
OrderItem objects.

**GET:** - **Permissions:** Supervisor and Staff. - **Supervisor:**
Retrieves order items belonging to orders associated with restaurants
managed by the authenticated user. - **Staff:** Retrieves order items
belonging to orders associated with the Staff member's restaurant. -
**Response:** Collection of OrderItem objects. - **Serializer:**
`OrderItemSerializer`

**POST:** - **Permissions:** Supervisor and Staff. - **Behaviour:**
Creates an OrderItem using submitted request data. - **Response:** Newly
created OrderItem object. - **Serializer:** `OrderItemSerializer` -
**Status Codes:** Supervisor creation returns `200 OK`; Staff creation
returns `201 Created`; validation errors return `400 Bad Request`.

------------------------------------------------------------------------

### 2. Order Item Detail

`api/detail_order_item/<int:order_item_pk>`

**Description:** Retrieves, updates or deletes a specific OrderItem.
Requires `order_item_pk`.

**GET:** - **Permissions:** Supervisor and Staff. - **Supervisor:**
Retrieves the specified OrderItem using Supervisor context passed to the
serializer. - **Staff:** Retrieves the OrderItem if it belongs to an
order associated with the authenticated Staff account. - **Response:**
OrderItem object. - **Serializer:** `OrderItemSerializer`

**PUT:** - **Permissions:** Supervisor only. - **Behaviour:** Fully
updates the OrderItem using submitted data. - **Response:** Updated
OrderItem object. - **Serializer:** `OrderItemSerializer`

**PATCH:** - **Permissions:** Supervisor only. - **Behaviour:**
Partially updates the OrderItem. - **Response:** Updated OrderItem
object. - **Serializer:** `OrderItemSerializer`

**DELETE:** - **Permissions:** Supervisor only. - **Behaviour:** Deletes
the OrderItem. - **Response:** `204 No Content`.

------------------------------------------------------------------------

### 3. Order Items Per Order

`api/order_items_per_order/<int:order_pk>`

**Description:** Retrieves all OrderItem objects associated with a
specific Order. Requires `order_pk`.

**GET:** - **Permissions:** Intended for Supervisor and Staff roles; the
current permission check should be reviewed. - **Behaviour:** Retrieves
OrderItem objects associated with the specified Order. - **Response:**
Collection of OrderItem objects. - **Serializer:** `OrderItemSerializer`

------------------------------------------------------------------------

### 4. Decrease Order Item Quantity

`api/order_menu_item_decrease/<int:order_item_pk>`

**Description:** Action endpoint for decreasing the quantity of a
specific OrderItem. Requires `order_item_pk`.

**DELETE:** - **Permissions:** Intended for Supervisor and Staff roles;
the current permission check should be reviewed. - **Behaviour:** - If
the quantity is greater than 1, decreases it by 1. - If the quantity is
1, deletes the OrderItem entirely. - **Response:** Confirmation message
and updated quantity. If the OrderItem is deleted, the returned quantity
is 0.

------------------------------------------------------------------------

## Other EndPoints

These endpoints provide supporting functionality for authentication,
session management, role identification and retrieving user-specific
information.

### 1. Get Logged-in User

`api/user_name`

**Description:** Retrieves information about the currently authenticated
user.

**GET:** - **Permissions:** Depends on the configured DRF permission
defaults; no explicit role restriction is shown in the view. -
**Behaviour:** Retrieves the user associated with `request.user` and
determines their assigned role. - **Response:** Username, primary key
and role (Owner, Supervisor or Staff). The role is `null` if the user
does not belong to one of these groups.

**Example Response:**

``` json
{
    "username": "example_user",
    "pk": 1,
    "role": "Owner"
}
```

------------------------------------------------------------------------

### 2. Create User

`api/create_user`

**Description:** Creates a new User account using
`StaffUserCreationSerializer`.

**POST:** - **Permissions:** No role restriction is explicitly enforced
in this view. - **Behaviour:** Validates the submitted user details and
creates a Django User if valid. - **Response:** Newly created user's
username. - **Serializer:** `StaffUserCreationSerializer` - **Status
Codes:** `201 Created` on success; `400 Bad Request` on validation
failure.

**Example Response:**

``` json
{
    "username": "example_user"
}
```

------------------------------------------------------------------------

### 3. Login

`api/login`

**Description:** Authenticates a user and establishes a Django session
using cookie-based authentication.

**POST:** - **Permissions:** No role restriction is explicitly enforced
in this view. Authentication uses the submitted username and password. -
**Behaviour:** - Uses Django's `authenticate()` function to verify the
supplied credentials. - If authentication succeeds, `login()` creates an
authenticated session. - Identifies the user's role through their
assigned Django group. - **Response:** Authenticated user's role and
username. - **Status Codes:** `200 OK` on success; `401 Unauthorized`
for invalid credentials.

**Example Response:**

``` json
{
    "role": "Owner",
    "username": "example_user"
}
```

**Authentication:** Uses Django session authentication. The frontend
must include `credentials: "include"` in subsequent Fetch API requests
so session cookies are sent.

------------------------------------------------------------------------

### 4. Logout

`api/logout`

**Description:** Logs out the currently authenticated user and
terminates their Django session.

**POST:** - **Permissions:** No role restriction is explicitly enforced
in this view. - **Behaviour:** Uses Django's `logout()` function to
terminate the current session. - **Response:** Confirmation message. -
**Status Code:** `200 OK`.

**Example Response:**

``` json
{
    "detail": "Successfully logged out"
}
```

------------------------------------------------------------------------

### 5. Get CSRF Token

`api/csrf`

**Description:** Retrieves a CSRF token required for protecting
state-changing requests made through the React frontend.

**GET:** - **Permissions:** No role restriction is explicitly enforced
in this view. - **Behaviour:** Uses Django's `get_token()` function to
retrieve a CSRF token and ensure the corresponding CSRF cookie can be
set. - **Response:** CSRF token. - **Status Code:** `200 OK`.

**Example Response:**

``` json
{
    "csrfToken": "example-csrf-token"
}
```

**Security:** The frontend should include the returned token in the
`X-CSRFToken` header when making requests requiring CSRF protection,
such as POST, PUT, PATCH and DELETE.

------------------------------------------------------------------------

### 6. Dynamic Time Greeting

`api/time_greetings`

**Description:** Generates a greeting based on the current local time.

**GET:** - **Permissions:** No role restriction is explicitly enforced
in this view. - **Behaviour:** Uses Django timezone utilities to
determine the current local hour. - **Response:** - Before 12:00 -- Good
morning - 12:00--16:59 -- Good afternoon - 17:00--20:59 -- Good
evening - 21:00 onwards -- Good Night - **Status Code:** `200 OK`.

**Example Response:**

``` json
{
    "greeting": "Good afternoon"
}
```

------------------------------------------------------------------------

### 7. Get All Supervisors

`api/get_supervisors`

**Description:** Retrieves users assigned to the Supervisor group.

**GET:** - **Permissions:** No role restriction is explicitly enforced
in this view. - **Behaviour:** Queries Django users belonging to the
Supervisor group and extracts their primary keys and usernames. -
**Response:** List of Supervisors. - **Status Code:** `200 OK`.

**Example Response:**

``` json
[
    {
        "id": 1,
        "username": "supervisor_one"
    },
    {
        "id": 2,
        "username": "supervisor_two"
    }
]
```

------------------------------------------------------------------------

### 8. Get Staff Restaurant

`api/get_staff_restaurant/`

**Description:** Retrieves the Restaurant associated with the currently
authenticated Staff user.

**GET:** - **Permissions:** Restricted to users belonging to the Staff
group. - **Behaviour:** - Retrieves the Staff object associated with
`request.user`. - Extracts the Restaurant linked to that Staff object. -
**Response:** Restaurant primary key and display name. - **Status
Codes:** `200 OK` on success; `403 Forbidden` if the user is not in the
Staff group.

**Example Response:**

``` json
{
    "restaurant_pk": 1,
    "restaurant_display_name": "Example Restaurant"
}
```

------------------------------------------------------------------------

### 9. Get Logged-in Staff Member

`api/get_staff_logged_in`

**Description:** Retrieves the Staff object associated with the
currently authenticated user.

**GET:** - **Permissions:** No explicit Staff group restriction is
enforced in this view. - **Behaviour:** - Uses `request.user` to
retrieve the corresponding Staff object. - Serializes the Staff object
using `StaffSerialiser`. - Returns the serialized Staff data and its
primary key. - **Response:** Staff object and its primary key. -
**Serializer:** `StaffSerialiser` - **Status Code:** `200 OK`.

**Example Response:**

``` json
{
    "staff_object": {
        "id": 1,
        "username": "example_user"
    },
    "staff_object_pk": 1
}
```

**Note:** The example illustrates the response structure. The actual fields inside `staff_object` depend on the fields defined in `StaffSerialiser`.


------------------------------------------------------------------------

## Future Improvements :
- Holiday requests from Staff, Superviosrs can approve or reject the holidays. (README.md 5 Nov 2026)