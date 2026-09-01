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
        - <button onClick = {FunctionName} >
Conditional rendering # Continue
Lists
Forms
useEffect
API requests
React Router