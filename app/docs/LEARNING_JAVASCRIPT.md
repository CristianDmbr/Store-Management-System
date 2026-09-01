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
        - A JavaScript object stores a key/value pair.
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
Template literals
Destructuring
Spread operator
Rest operator
Array methods
.map() ***
.filter()
.find()
.reduce()

Level 3:
DOM
Events
Buttons
Forms
Inputs
addEventListener
document
querySelector

Level 4
HTTP
fetch()
JSON
GET
POST
PUT
PATCH
DELETE
async
await
Promises
try / catch

Level 5 :
Export and Import

Level 6:
Components
JSX
Props
State
useState
Events
Conditional rendering
Lists
Forms
useEffect
API requests
React Router