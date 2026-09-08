## Learn JavaScript

# What is JavaScript
Its a programming language used to make a website and web applications interactive and dynamic.
If HTML it just makes a button :
<button>Click me</button>
JavaScrip can make something happen when you click it:

button.addEventListener("click", function() {
    alert("Hello!");
});

So : 
HTML -> Structure
CSS -> Appearance
JavaScript -> Behaviour / Logic

JavaScript can also be ran outside of the browser using the Node.js environment.
e.g. : 
Frontend : JavaScript / React
Backend : JavaScript / Node.js

Script : is a program / instructions that tell a computer to perform a sequence of actions. (A script can be any language e.g. print("Hello World") is a script)

Why is it called JavaScript?
Historically the term "script" was used because JavaScript was designed to be embedded into webpages and executed by the browser.
It has nothing to do with Java.

# Difference between using Python and JavaScript
Currently : Browser -> HTML templates -> Django -> Python -> Database
JavaScript : Browser -> React/JavaScript -> HTTP reequest -> Django API -> Database

So with React, much more of the interface logic is moved into the browser so Django doesn't generate much of the entier webpage anymore. So React received data from Django and creates the interface.

With the API views, the Django project can communicate using JSON and JavaScript can communicate with that API and React Can display it.

<const reponse = await fetch("/api/order_list");
const orders = await response.json();
console.log(orders) >

# Differences between Python and Java
Numbers:
left x = 10 and let y = 10.5 are both considered numbers and JavaScript does not distinguish.

Booleans:
<let is_staff = true> (yes small letters)

Arrays:
Python : <orders = [1,2,3]>
JavaScript : <let orders [1,2,3]>

Dictionary:
Python :
order = {
        "pk" : 1,
        "status" : "waiting"
}

JavaScript :
const order = {
        pk : 1,
        status: "waiting"
};

Functions:
python:
<def add(a, b):
        return a + b>

JavaScript
<function add(a, b) {
        return a + b;
};>

# Huge JavaScript concept Asynchronour programming
Biggest thing to need for React and APIs. Django API takes time to respond. React waiting for orders
So JavaScript has concepts of:
Promise, async, await

# Creating variables
Declaring a variable in JavaSript using let, const, var

Python:
< name = "Cristian"
age = 20 >

< JavaScript:
let name = "Cristian";
const age = 20;
var city = "London"; > 
(The important difference is whether the variable can be reassigned and how its scope behvaes)

let : Create a variable whose value I can change later
e.g.
< let age = 20;
age = 21
console.log(age) -> 21 >
Also change the type
<let thing = 10;
thing = "hello";
thing = true;
>

const : Create a variable that you don't intend to reassign
<const name = "Cristian";>
if you try <name = "John";> it will create an error
<const response = await fetch("/api/order_list");>

var : Older day of declaring variables
var does allow us to change the variable but it has a scoping behaviour.
e.g. if we did
if (true) {
        let x = 10 or const x = 10;
}
console.log(x) would give us an error because the x only exists inside the {} scope not outside.

BUT
if (true) {
        var x = 10;
}
console.log(x) 
Will work.
GENERALLY DON'T USE VAR

One important concept with const
e.g.
const person = {
        name : "Cristian",
        age : 20
};
person.age = 21 it works because const prevents from reassigning the variable itself, it DOESNT make the object immutable
so
< const person = {
    name: "Cristian"
};

person = {
    name: "John"
};>
Its not allowed

# Using ;
Use ; to indicate where the statement ends.
Its a code style choice.

# Differences in JavaSCript dictionaries.
In both Python and Json
We have
{
        "name" : "Cristian",
        "age" : 20
}

But in JavaScript you can have the key objects either with "" or without. But for some key names add the "".
e.g. 
< const person = {
        name = "Cristian";
        "first-name" = "Cristian";
};
>

# Access object properties
You can do either order.pk (DOT PROPERTY) or order["status"]

############################################################
PHASE 1 — JavaScript Fundamentals
        ↓
PHASE 2 — Functions & Scope
        ↓
PHASE 3 — Arrays & Objects
        ↓
PHASE 4 — Modern JavaScript (ES6+)
        ↓
PHASE 5 — DOM & Browser
        ↓
PHASE 6 — Async JavaScript & APIs
        ↓
PHASE 7 — Modules & npm
        ↓
        ⭐ JAVASCRIPT READY
        ↓
PHASE 8 — React

############################################################
Level 1 :
Variables
let / const
        - let allows to modify variables
        - const doesn't (but if a object is a const that doesn't mean we cannot mutate it)
        - var old fashioned and it doesn't respect the scope rule
Data types
        - Finding the datatype of a object use
        - <typeof 20> -> Number
        - <typeof true> -> Boolea
Strings
        - Can use " " and ' '.
        - A string can contain multiple words <cont restaurat = "My Italian Restaurant">
        - Combining string :
          - < const firstName = "Cristian"; const lastName = "Dumbravanu"
          - const fullName = firstName + " " + lastName>
        - Template literals (Dynamic Strings)
          - < const name = "Cristian";
          -   const age = 20;
          -   console.log(`My name is ${name} and I am ${age}`)> USE ` NOT '
Numbers
        - No seperate types like int or float
        - operations are the same as Python
Booleans
        - Lower Case : true or false
        - <const isSaff = true;>
Arrays
        - Collection/list of values
        - Python <orders = [1,2,3];>
        - JavaScript <const orders = [1,2,3]; or const restaurants = [ "KFC", "McDonald's", "Pizza Hut"]; >
          - You can access using index:
          - <console.log(restaurants[0]);>
        - Arrays can contain different datatypes
        - append() == push()
        - insert(0,x) == unshift(x)
        - pop() == pop()
        - pop(0) == shift()
        - len(arr) == arr.length
        - arr[0] == arr[0]
        - arr[-1] == arr[arr.length - 1]
        - x in arr == arr.includes(x)
        - arr.index(x) == arr.indexOf(x)
        - arr.remove(x) == arr.splice()
        - arr.sort() == arr.sort()
        - arr.reverse == arr.reverse()
Objects
        - A JavaScript/Python object stores a key/value pair.
        - Say the Django API returns this Jason
                [
                {
                        "pk": 1,
                        "status": "waiting"
                },
                {
                        "pk": 2,
                        "status": "not_been_served"
                }
                ]
        - Once JavaScript has parsed this JSON :
        - const orders = [{
                                pk: 1,
                                status: "waiting"
                          },
                          {
                                pk: 2,
                                status: "not_been_served"
                           }
                           ];
        - Accesing the object properties using dot notation <order.pk> or bracket notation <order["status"]>
        - (Remember that with const it prevents you from replacing the variable but it still lets you modify it's properties)
        - e.g. 
        - < const order = {
                status : "waiting"};
            order.status = "served" > Is allowed
        - <order = {
              - status = : "cancelled"};> is NOT allowed 
        - A object can have an array
        - <const person = {
                nums : [1,2,3,4] };
           person.nums[1] -> 2 >

        - Objects can contain other objects
        - <const person = {
             address : {
                city : "London",
                postice : "RM12",
             }}
                person.address.city>

if / else
        - Differemces elif == else if, == is ===
        - and == &&
        - or == ||
        - not !
        - () around the condition
        - {} instead of indentation
        - Python :
        - <age = 20
         if age >= 18:
                print("Adult")
          elif age >= 13:
                print("Teenager")
          else:
                print("Child")>
        - JavaScript :
        - < let age = 20;
            if (age >= 18) {
                console.log("Adult);
            } else if (age >= 13) {
                console.log("Teenager");
            } else {
                console.log("Child");
            }
         >

for loops
        - Python
        - <for fruit in fruits:
                print(fruit) >
        - JavaScript:
        - <let fruites = ["apple","banana","orange"]
        - for (let fruit of fruits) {
           console.log(fruit) }>
        - Looping through numbers
        - Python  < for i in range(n):
            print(i) >
        - JavaScript < for (let i = 0; i < 5 ; i++) {
          console.log(i) } -> 0,1,2,3,4 
         >
        - Follows a (Starting Point, Condition, Increment) 
        - Looping using indexes
        - < let fruits = ["apple", "banana","orange"]
            for (let i = 0; i < fuits.length; i++){
                console.log(fruits[i])
            }  > 
while loops
        - Python
        - <i = 0
           while i < 5:
                print(i)
                i += 1 >
        - JavaScript
        - <let i = 0
           while (i < 5) {
                console.log(i);
                i ++;
           } >
        - break is used the same in a ()
        - if (i == 5) {
          break }
        - continue is used the same
        - if (i == 5) {
          continue; }
Functions
        - Python:
        - <def greet():
          - print("Hello")>
        - JavaScript:
        - <function greet(){
          console.log("Hello");
          }>
        - <greet();> 
        - Or with parameters
        - <function greet(name, surname){
                console.log("Hello there" + name + " " + surname);}>
return
        - For printing <console.log()> for returning <return something>
        - Once we do return it stops the rest of the function

Level 2 :
Arrow functions
        - Normal Function
        - < function add(a,b) {
            return a + b; }
        - >
        - Arrow Function:
        - <const add = (a, b) => {
             return a + b;
         }>
        - Both do the same thing
        - Structure :
        - const functionName = (parameters) => { code }
        - Short Arrow Function :
        - With the arrow functions you can remove the {} and return function
        - Instead of < const double = (number) => {
             return number * 2; }; >
        - It can become
          - <const double = (number) => number * 2 > 
        - In React you will see :
        < const handleClick = () => {
                return ( <h1> Hello World </h1>)
        } > 

Template literals
        - Uses backticks ` instead of ' or "
        - Normal String
        - < const name = "Cristian";
        -  console.log("Hello" + name)>
        - Template Literal
        - < const name = "Cristian";
        - console.log(`Hello ${name}`)>
Destructuring
        - Used to deconstruct values in a Structure.
        - e.g.
        - <const person = {
                name : "Cristian";
                age : 21; };
           const {name, age} = person>
        - Names need to match the key values. But if you want to rename "
        - const { name : userName, age : userAge} = person
        - e.g.
        - const numbers = [10,20,30]
        - const [first,second,third] = numbers
        - Dictionaries by property names, Arrays by positions 
Spread operator
        - ... take the contents of something and spread it out in another place.
        - It can be used to 
        - e.g. let numbers = [1,2,3];
        - 1. Copy an array:
        - const newNumbers = [...numbers] -> [1,2,3]
        - 2.Combine arrays
        - const otherNumbers = [4,5,6]
        - const newNumbers = [...numbers, ...otherNumbers]
        - 3. append or insert either at the beggining or the end of an array
        - const newNumbers = [0,...numbers] # At the begining
        - const newNumbers = [...numbers,4] # At the end
Rest operator
        - Also uses ... to gather things together inside of an array
        - e.g.
        - < function add(...numbers) {
          - console.log(numbers)
        - }
        - add(1,2,3,4)> -> [1,2,3,4]
        - e.g. Multiple parameters
        - < function introduce(name, ...hobbies) {
          - console.log(name);
          - console.log(hobbies);
        - } 
        - introduce("Cristian","coding","gaming","reading")> -> Cristian, ["coding","gaming","reading"]
Array methods
        - push(), pop(), shift, unshift ...
.map() 
        - goes throught every item in an array and creates a new array by transforming each item
        - < const numbers = [1,2,3,4]
        -   const double = numbers.map(number => number * 2);>
.filter()
        - Goes through an array and keeps only the items that satisfy a condition.
        - < const numbers = [1,2,3,4,5]
        -   const bigNumbers = numbers.filter(number => number > 3);> -> [4,5]
.find()
        - Similar to filter but only returns the first item that satisfies the condition
        - < const numbers = [1,2,3,4,5]
          - const result = numbers.filter(number => number > 3)> -> 4
.reduce()
        - Takes all items in an array and reduces them down to one final value
        - Go through the array, keep a running result and update that result for every item and at the end return one value.
        - e.g.
        - < let nums = [1,2,3,4]
             const total nums.reduce(
                (accumulator, currentValue) => accumulator + currentValue,
                0
             ) >
        0 represents the initial accumulator value and will become the final result
        currentValue is the value we are currently over.

# Where JavaScripts starts to interact with an actual webpage.
Level 3:
DOM
        - Document Object Model (JavaScript's representation of a HTML page)
        - e.g.
        - <h1>Hello</h1>
          <p>Welcome to my website</p>
          <button>Click me</button>
        - The browser turns that HTML into a structure JavaScript can interact with and then say:
          - Find that button, Change the heading, remove the paragraph, add something to the page
        - <h1 id = "title">Hello</h1>
        - < const title = document.getElementById("title"); >
        - So now title refers to the <h1> element
        - So you can say modify it to title.testContent = "Hello Cristian";
Events
        - Events is what happens on a webpage (Clicks button, types something, moves their mouse, submits form, loads page...)
        - JavaScript can listen for these events and then it does something
Buttons
        - Suppose we have:
        - <button id = "myButton"> Click Me</button>
        - we can find it :
        - <const button = document.getElementById("myButton");>
        - And add a function
        - <button.addEventListener("click",function() {
          - console.log("Button clicked!");
        - })>;
        - A more complex example:
        - < const title = document.getElementById("title");
            const button = document.getElementById("button");

            button.addEvenListener("click", ()) => {
                title.textContent = "You clicked the button!";
            }
        - >
        - we can print the even to find the even type
        - Also event.target we can also get the element which changes because of an event.
        - Main events : click, input (user changes an input, typing in a box), change (checkboxes or dropdowns), submit (login, form is submitted)
Forms
        - Not the Django form. Its the HTML form which allows users to enter and submit information
        - <form>
          - <intput type="text">
          - <button>Submit</button>
        - </form>
Inputs
        - A place for users to enter or select information.
        - type = text, number, password,email
addEventListener
        - When this even happens to this element, run this function
document
        - Representation of the current HTML page as a object representation of the page called DOM.
        - JavaScript gets access to the DOM through document.
        - So document is the current webpage
querySelector
        - Its used to find HTML elements
        - We can do document.querySelector("h1") to get all h1 elements
        - But we can add a # in front to get the elements based on ID
        - <h1 id="title">Hello</h1>
        - document.querySelector("#title")
        - if you add . it can be used to find by class.

Level 4
HTTP
fetch()
        - JavaScript's way of making requests
        - e.g. fetch("api/"order_list"); means JavaScript makes an HTTP request to /api/order_list
        - By default its a GET
        - The problem is that the request does not respond instantly:
        -  JavaScript (GET) -> Django (backend for the query and serializer and response) -> Back to JavaScript
        -  Java Script cannot freeze the entire website while waiting
        -  JavaScript just says "I will deal with the request and when the response arrives I will deal with it"
        -  This is where Promises come in.
JSON
GET
POST
PUT
PATCH
DELETE
async
        - Async tells JavaScript that this function will perform asynchronous work (SOMETHING CAN TAKE TIME WIHTOUT STOPPING EVERYTHING ELSE)
        - < async function getOrder(){ } >
        - Used on functions
await
        - awaits says "Wait for the promise to finish before continuing this function"
        - Used for HTTP request
        - <async function getOrders() {
            const response = await fetch("/api/order_list");
            const data = await response.json();
            console.log(response);
        -  }>
        -  This means : wait for the get to finish, once finished put the result into response and then display the response but this while function will take time but wont stop anything
Promises
        - A placeholder for future request throught JavaScript(Like explained earlier)
        - e.g. You order a burger and you don't get the burger immediatelly but instead an equivalent of "Burger is coming".
        - This promise can eventually become the fulfilled request or the Rejection and reason.
try / catch
        - try {Code that might fail}
        - catch {What to do if it fails}
  
Full Function Example:
< async function getOrders(){
        try {
                const response = await fetch("api/order_list");
                const data = await response.json();
                console.data(data);
        } catch (error) {
                console.data("Error", error);
        }
}

>

Level 5 :
Export and Import
e.g.
You have a math.js file and inside:
<function add(a,b) {
        return a + b
}>
Then you have another file app.js
How does app.js use the add function ?
Export the function from inside
< export function add(a,b) ... >
inside app.js:
import { add } from "./math.js";
console.log(add(2,3));

Same can be done with variables
Inside math.js <export const restaurantName = "KFC";>
Inside app.js <import { restaurantName } from "./restaurant.js";>

Level 6:
Components
        - Reusable piece of UI
        - < function Order(){
            return <H2>Order</H2>
           }
        - >
        - We can use it as <Order />
JSX
        - JavaScript syntax that lets you describe UI using HTML-like elements.
        - (Reuse your HTML knowledge)
        - < function Order(){
          - return (
            - <div>
              - <h2>Order 1</h2>
              - <p>Table 5</p>
            - </div>
            - );
        - } >
Props
        - How you pass information from one component to another.
        - <function Order(props){
           return <h2>Order #{props.id}</h2> 
        - }>
        - Dynamically adds the id
State
        - Information that React remembers for a componet and that can change
        - e.g. button clicked 1 or 2 times.
        - "This value changes so update the UI"
useState
        - How you create a state
        - < const [count, setCount] = useState(0) >
Events
        - Similar to the JavaScript listener
        - In HTML:
        - <button onClick = {FunctionName} > Click Me </button>
Conditional rendering
        - Showing different UI based on the condition.
Lists
        - Say we have:
        - consts orders = [
           { id : 1, table : 5 },
           { id : 2, table : 2} 
          - ];
        - In React we can do
        - {orders.map(order => (
          - <p key = {order.id}>
                Order #{order.id} - Table {order.table}
            </p>    
        - ))}
        - We only need the key for REACT to display
        - So map goes throught each object in the array one at a time.
Forms
        - Need To Learn
useEffect
        - " Run some code when something happens/changes in the component lifecycle "
        - < useEffect(() => {
          - getOrders();
        - }, []
        - )>
        - Means Run getOrders when this component "[]" loads.
        - This connect Api's so React
React Router
        - Lets you have different pages/views in the React Application
        - e.g.
          - / -> DashBoard
          - /order -> Orders
        - Create routes :
          - <Route path="/orders" elements={<OrderList />}/>
          - So at the /orders it will show the OrderLis components
  
npm -> Manages JavaScript packages
pip -> Manages Python packages
Vite is the tool that creates and serves the frontend during the development

.jsx is what allows us to write HTML components inside of JavaScript
.js just JavaScript

# Starting JavaScript and React

Inside App.jsx:
<function App(){
        ...
}
export App>
App is not the Restaurant Management Application, its a React component/function.

A React Component : piece of Website/UI e.g. NavBar, SideBar, RestaurantCard, MenuItem ...
e.g.
<function RestaurantCard() {
    return (
        <div>
            <h2>Mario's Restaurant</h2>
            <p>London</p>
        </div>
    );
}>
Similar to how we can have JavaScript functions which say add parameters we have a function which returns JSX that would appear on the webpage.

Where does the App() component get used?
Inside the main.jsx we have <import App from './App.jsx'> which means "Get the component called App from the App.jsx".
We can use it with <App />
Why does the <App /> look like HTML? because its JSX so its a React component not a HTML component

Purpose of <export default App;> is to allow other JavaScript files to import this component. "Make this available to other files"

# What is Vite?
Development tool for the frontend which helps develop your React application.
So when you run <npm run dev> to start the localhost for the frontend it means "Vite, start my React development environment" and Vite starts http://localhost:5173

# Why does http://localhost:5173 work without having to run Django?
<npm run dev> : Vite -> React frontend -> http://localhost:5173
<python manage.py runserver> : Django -> Backend/API -> 127.0.0.1:8000
They are completely independent.

# Do they need to run simultaneously?
When you are developing the full React + Django application, Yes. (Use two terminals)
So it will become : Browser -> React/Vite (localhost:5173) -> fetch() -> Django/ DRF (127.0.0.1:8000) -> DataBase

# How can React work without Django?
Since the only component we have is :
<function App() {
    return <h1>Hello from my restaurant system!</h1>;
}>
There is no request to Django

# Why have different .jmx files e.g. for RestaurantList? 
App.jsx is where components from other files get sorted / organised and then rendererd. (Main root)
Other files are useful since there will be a lot of components

# What is a <div>?
A container for grouping HTML elements.
Think of it as a box and you can add CSS to style that box

<div className = "restaurant-card">
In CSS:
.restaurant-card {
        border : 1px solid black;
        padding : 20px;
}

# Get Restaurants from Django
I already </api/my_restaurants/> and the Django API is responsible for querying the database.
REACT DO NOT DIRECTLY QUERY YOUR DJANGO DATABASE.

React -> HTTP request -> Django API -> Django queries database -> Serializer -> JSON -> REACT
(Architecture rule)

Django will return:
[
    {
        "pk": 1,
        "restaurant_name": "Mario's",
        "location": "London",
        "restaurant_cuisine": "Italian"
    },
    {
        "pk": 2,
        "restaurant_name": "The Grill",
        "location": "Romford",
        "restaurant_cuisine": "Steakhouse"
    }
]

REACT only requests and displays the data.

# Summary
1. We have a RestaurantList.jsx file which containts reusable React components.
2. We then have a Restaurants.jsx to display all of these components and structure them.
3. We use the App.jsx to generate and route.

# Have multiple React Component in one jsx page when they go together when exporting.

# Understand my first React Function :
########################################################################
# Importing the two functions from the React library.
< import { useState, useEffect } from "react";

# RestaurantList describes what should appear on the screen.
function RestaurantList() {

    # useState is a React function and in this case we give it []
    # Means "React I want to create some state, and its starting value should be an empty array."
    # State : data that belongs to a component and can change over time. (In this case we fill it with Restaurant objects)
    # Why [restaurants, setRestaurants] ? desctructuring where restaurants is the current value, setRestaurants is the function used to change that value.
    # So create a state. Set the current value to be restaurants, and give me a function called setRestaurants that changes it.
    const [restaurants, setRestaurants] = useState([])

    # useEffect means "React after rendering this component, perform this piece of code."
    useEffect(() => {
        # fetch is used to make HTTP requests. Its GET by default. 
        # fetch() doesn't give you the data immediatelly, its a Promise that its working on getting the result and it will give me the result one its ready.
        fetch("http://127.0.0.1:8000/api/my_restaurants/")
            # Could also be .then(x => x.json())
            .then(response => response.json()) # This is a arrow function meaning the response from this promise gets converted to a body usabel by JavaScript.
            # After previous operation has finished and the produced JSON data, give that data to this function. (Output from previous arrow function is called data).
            # Fills the useState array with objects.
            .then(data => {
                setRestaurants(data); # Where the API data gets put into the React state. (Initially its a empty array []) 
            });
    }, []); # This [] means the dependency array. Ignore for now
    1. RestaurantList appears
    2. React Renders it. useEffect runs the code
    3. React renders again
    4. Displays the restaurants

    return (
        <div>
            <h1>My Restaurants :</h1>
            # Since restaurants is the useCase which is an array.
            # .map() is a JavaScript array method means "Go through every item in an array and create something from each item."
            # In the restaurants array go through each restaurant (variable name) and have its key and its name, location and cuisine.
            {restaurants.map(restaurant => (
                # Helps represent each restaurant with something in this case its the pk
                <div key = {restaurant.pk}>
                    <h2>{restaurant.restaurant_name}</h2>
                    <p>{restaurant.location}</p>
                    <p>{restaurant.restaurant_cuisine}</p>
                </div>
                # Why two divs? each has its purpose
            ))}

        </div>
    );
};

export default RestaurantList>
# default means its only imported as < import RestaurantListfrom from "./RestaurantList"; >
if we do export {RestaurantList};
# It will allow for import { RestaurantList } from "./RestaurantList";
########################################################################

# useState : Lets a React component store data that can change with a function you named that specific datatype.
const [age, setAge] = useState(18); age is current age, setAge is the function to modify, 18 is the starting value.
< setAge(19); >

# useEffect : lets you run code as a side effect of a component being rendered.
useEffect(() => {code}, [])

# .then : since fetch is a promise, then means run this function once promise is finished
find(url)
        .then(response => response.json())
        .them(data => restaurants(data);)

# .map() : goes through every item in an array and creates something for each item.
restaurants.map(restaurant => (HTML))

# Make React authenticated with Django session cookies
Since when we make a request to get the Restaurant list from the Collection of Restaurant's API using fetch and then running it at < http://localhost:5173 >
Browser considers them different origins.
We need to make cross-origin requests and allow credentials. "Include my django session cookie with this request".
< pip install django-cors-headers > Followed AI tutorial
After updating the settings.py:
<    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/my_restaurants/", {
            credentials : "include"        ## Add this. Include cookies when making this request
        })>

# How authentication from Django now works on React?
Cookies/session authentication is what allows React to be recognised by Django as a logged in user.
The Browser stores the Django session cookies so its the Browser that holds the cookies.
After the modification to the settings.
1. When React makes the API request:
< fetch("http://localhost:8000/api/my_restaurants/", {
    credentials: "include"
}) >
credentials : "include"
Tells the browser that "When making this request, include the relevant cookies from this browser"

# Rendering in Django
I did not make a HTML template but there is a HTML file just not made by me.
Once we try to render the App.jsx React creates a DOM and it renders in the Browser.

# Creating a Greetings component
I had to make a seperate Django API endpoint to get me the user.



