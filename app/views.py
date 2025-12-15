from django.shortcuts import render,redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


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

        #title = request.POST.get("title")
        #status = request.POST.get("status")
        #assistance = request.POST.get("assistance")
        #due_date = request.POST.get("due_date")
        #if title :
            #Task.objects.create(title = title, status = status, assistance = assistance, due_date = due_date) 
        #return redirect("task_list")
    
    #tasks = Task.objects.all().order_by("-id")
    #return render(request, "tasks/task_list.html",{"tasks" : tasks})

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