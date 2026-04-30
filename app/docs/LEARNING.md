**You need markdown extension to process and format the markdown text.**

# What is the {% csrf_token %}?
- Inserts a hidden input input into the HTML form containing a protection of your form from submisions from malicious requests from other websites.

# What are migrations ?
- Migrations translate Python models into real database tables and fields and keeps database structure in sync with your code.
- Python @properties to the models do not require any migrations because only exists in the Python Memory and they do not change databse column so when you try to mitigate Django sees nothing to mitigate

(Extension used : Markdown All In One)

# What is a MarkDown? :
- A lightweight text formatting language that lets you write plain text and convert it into structured, styled documents (heading, lists or bold text).
- Text to HTML conversion tool for web writers.
- MarkDown is not a replacement for HTML, it only uses small elements so its very simple to use.
- The point of MarkDown is to help read and write.

# MarkDown Formations# :
- Heading 1, ## Heading 2, ### Heading 3
- For italics, ** Bold
- Unordered Lists *, +, - 
  -Ordered Lists 1 ... n

# APIs
What is an API : Is a way for programs to talk to each other.
What are they used for : send data, get data and connect apps. e.g. : Website asks backend for all restaurants so backend send it and they communicate through API.
How do they work? 
1. Cliend (browser/app) sends a request (Give me menu items)
2. Backend receives it, Django view, API processes it.
3. Backend sends a response (usually JSON) e.g. {"name" : "Pizza"}

Where  I could use it:
Right now: Django views return the HTML templates.

With APIs:
Django will return data (JSON) instead which allows for mobile apps, react frontends and other systems to use the backend.