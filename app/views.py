from django.shortcuts import render,redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    tasks = Task.objects.all().order_by("-id")
    return render(request, "tasks/task_list.html",{
        "tasks":tasks,
        "form" : form,
    })

def complete_task(request, task_id):
    task = Task.objects.get(id = task_id)
    task.completed = True
    task.save()
    return redirect("task_list")


def delete_task(request, task_id):
    # Safely get the task or return a 404 page if it doesn't exist
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")

def all_tasks(request):
    tasks = Task.objects.all().order_by("-id")
    return render(request, "tasks/all_tasks.html", {"tasks" : tasks})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html",{"form": form})

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username = request.POST["username"],
            password = request.POST["password"]
        )

        if user:
            login(request, user)
            return redirect("task_list")
        else:
            error = "Invalid username or password"
            return render(request, "auth/login.html",{"error" : error})
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")