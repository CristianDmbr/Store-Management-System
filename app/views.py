from django.shortcuts import render

def home(request):
    context = {"submitted": False}  # initially nothing submitted

    if request.method == "POST":
        context["name"] = request.POST.get("name")
        context["surname"] = request.POST.get("surname")
        context["age"] = request.POST.get("age")
        context["country"] = request.POST.get("country")
        context["submitted"] = True

    return render(request, "greetings/home.html", context)