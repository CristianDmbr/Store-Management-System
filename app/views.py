from django.shortcuts import render

def home(request):
    context = {"submitted": False}  # initially nothing submitted

    if request.method == "POST":
        context["username"] = request.POST.get("username")
        context["real_name"] = request.POST.get("real_name")
        context["email_adress"] = request.POST.get("email_adress")
        context["number"] = request.POST.get("number")
        context["time"] = request.POST.get("time")
        context["submitted"] = True

    return render(request, "greetings/home.html", context)