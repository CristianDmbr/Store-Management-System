from django.shortcuts import render

def info(request):
    context = {"submitted" : False}
    if request.method == "POST":
        context["name"] = request.POST.get("name")
        context["surname"] = request.POST.get("surname")
        context["submitted"] = True
    
    return render(request, "greetings/home.html", context)