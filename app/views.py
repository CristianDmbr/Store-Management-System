from django.shortcuts import render

def home(request):
    name = None
    if request.method == "POST":
        name = request.POST.get("name")
    return render(request, "greetings/home.html",{"name": name})