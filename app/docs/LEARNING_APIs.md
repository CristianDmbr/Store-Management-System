## Learning APIs

# What problem does an API solve?
Imagine you have a restaurant management system on a server. It has a database/backend of Users, Restaurants, Staff etc ... .
All types of clients (Mobiles, Computers) use APIs. But say when wanting to have a React website frontend, React cannot use the render(request,...., context) it needs to receive data from the backend in a JSON format. (That is where APIs come in)
It uses API functions (Not CBV or FBV).

When working with REACT as the FrontEnd CBV and FBV are useless since we do not use them.
CBV and FBV are only used for rendering HTML, and it was a great way to learn Django and Webdevelopment concepts.

Existing Application:
Django - 
    - Models
    - Forms
    - FBVs
    - Templates

Goal:
Django -
    - Models
    - Serializers
    - DRF views
    - REACT

Database, Models, Relationship, Authorization and business Logic does not change. Only the interface between the client and backend/database.

# ENDPOINT
A URL exposed by your backend for a particular operation/resource. Doorway into backend.
e.g. :
    /api/restaurants/
    /api/restaurants/5/

HTTP tells the backend what you want to do
GET - retrieve
POST - create
PUT/PATH - update
DELETE - delete

# What will happend to forms?
Forms are designed to handle HTML, with APIs we will use serializers.
Since the final frontend is React and the backend will be API only, forms will no longer be needed.
(They taught me Django's validation and form_processing system)

HTML -> Forms        REACT -> DRF serializers

# Was it useless what I did?
No, I have designed an application and now I will learn how to expose it to another client.
# Can I skip FBV for my next Project?
Yes if it will be a React Frontend + Django backend

Plan :
1. Django Models
2. DRF serializers
3. DRF API views
4. API endpoints
5. REACT
   
# What is REACT ?
Not a replacement for HTML.
Its a JavaScript ( a programming language used to make interactive webpages ) library for building user interfaces.

In Traditional Django it will generate templates but with REACT it will let us build interfaces using reusable components.
1. React
2. GET /api/restaurants/5/
3. Django
4. JSON (From DRF views and serializers)
5. REACT
6. Updates Dashboard

So REACT is a tool for building complex interactive web interfaces using JavaScript components

# Serializers
Serializers is the component that translates between Django/Python objects and API data.

Django Model Object -> Serializer -> JSON
JSON from react -> Serializer -> Validated Django data -> Django Model

Three Main Jobs:
1. Serialize:
   Django Object -> Serializer -> JSON-friendly data
2. Deserialisation:
   JSON -> Serializer -> Python validated data
3. Validate
    def validate(self, attrs)

# My confusion about the different Stacks
1. FBV + CBV -> Forms -> Django Templates (HTML)
Django FBV + CBV -> render() -> HTML Template(html) -> Browser
2. Django REST Framework (DRF) : when you want the backend to communicate with separate technologies (e.g. React) use APIs, DRF allows to build API views which communicate with other technologies using the JSON format (Uses serializers)
Django + DRF -> Serializers -> JSON -> React/JavaScript
3. JavaScript and React : JavaScript is a Programming Language, React is a JavaScript library used to build user interface.
JavaScript can manipulate the data (How it presents the data) and chose how its displayed on REACT.

# JSON.stringify()
Say we have a JavaScript object
{
    username : username,
    password : password
}

JSON.stringidy converts the JavaScript object into a JSON string so it can be sent in the HTTP request body.
To see the JavaScript/React terminal we need to see it on the browser 

# Pass url parameters in JavaScript
e.g. passing the restaurant pk to another page.
Make the route : {
    <Route
          path = "/restaurant_info/:restaurant_pk"  
          element = {<RestaurantInfo/>}
        />
}
:restaurant_pk is the parameter.
Pass it to another page: 
<<button onClick={(event) => navigate(`/restaurant_info/${restaurant.pk}`)}>View details</button>>
make sure to use `` and ${}.

To receive that query parameter:
<const { restaurant_pk } = useParams();>
Ensure the naming matches with the app route naming of variables.

# Problem during development.
In my UpdateRestaurant REACT page. ONCE I made the PUT request if I was to navigate straight away then the update would not have been finished yet and the restaurant list still would show the old data. So instead of relocating straight away make a function which will wait for the update completion.
< .then(() => navigate("/restaurant_list")); > 

# Learn reduce 
<const numbers = [1,2,3,4];>
<numbers.reduce(...)>
To take an array and build something else from it.
We start with an empty object : 
{}
Starters arrive : {starter : [starter item]}
Main Arrives : {
    starter: [starter item],
    main: [main item]
}
Another starter arrives: {
    starter: [starter item, another starter],
    main: [main item]
}

Example :
<    const groupedMenuItems = menu_items.reduce((groups, menu_item) =>{
        
        if ( !groups[menu_item.category]) {
            groups[menu_item.category] = [];
        }

        groups[menu_item.category].push(menu_item);
    
    }, {});>

# What is reduce? 
Take an array and repeatedly build one final value from it.
e.g. we have an array of menu items.
We want to take each item and sort them by category :

{
    starter: [
        { name: "Soup", category: "starter" },
        { name: "Salad", category: "starter" }
    ],
    main: [
        { name: "Steak", category: "main" }
    ],
    dessert: [
        { name: "Cake", category: "dessert" }
    ]
}

In menu_items.reduce((groups,menu_item))
What is groups? 
groups = accumulator (Object we built so far)
menu_item = current item

Why not do (!groupedMenuItems[menu_item.category])?
Because groupedMenuItems does not exist yet since we have to run the code in reduce(...) Once final object is done assing it to GroupedMenuItems
The {} at the end refers to the groups should start as an empty OBJECT
Simple explanation:
{} is the object we are currently building. Declared at the begining. It then becomes groups["starters"] : []
{
    "Starters" : [],
}
then 
{
    "Starters" : [],
    "Mains" : []
}

At the end the completed groups gets assigned to groupedMenuItems.

# How to access a reduce object?
groupedMenuItems.starter or groupedMenuItems.main
