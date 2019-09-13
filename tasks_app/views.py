from django.shortcuts import render, get_object_or_404, redirect
import datetime
from .models import *
from .forms import *
# Create your views here.

def home(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    tasks = Task.objects.all()
    days = Day.objects.all()
    goals = Goal.objects.all()
    return render(request, "home_tasks.html", {"tasks":tasks, "days":days, "goals":goals})

def add_goal(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/')             # Finally, redirect to the homepage.

def remove_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be removed
    if request.method == 'POST':         # If method is POST,
        task.delete()    
        return redirect('/')             # Finally, redirect to the homepage.     
    
def task_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be removed
    if request.method == 'POST':         # If method is POST,
        task.task_done = True
        task.save(update_fields=["task_done"])
        return redirect('/')             # Finally, redirect to the homepage. 

def remove_goal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)  # the task to be removed
    if request.method == 'POST':         # If method is POST,
        goal.delete()    
        return redirect('/')             # Finally, redirect to the homepage.    

def add_task_to_daily_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be added
    if request.method == 'POST':         # If method is POST,
        # add task to dayily tasks
        # the get_or_create method is that it actually returns a tuple of (object, created). 
        # The first element is an instance of the model you are trying to retrieve 
        # and the second is a boolean flag to tell if the instance was created or not. 
        # True means the instance was created by the get_or_create method and 
        # False means it was retrieved from the database.
        day = Day.objects.get_or_create(date=datetime.date.today())[0] 
        day.daily_tasks.add(task)
        day.save() # Django doesn’t hit the database until you explicitly call save().
        return redirect('/')             # Finally, redirect to the homepage.

def remove_task_from_daily_tasks(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # the task to be added
    if request.method == 'POST':         # If method is POST,
        # remove task from dayily tasks
        day = Day.objects.get(date=datetime.date.today())
        day.daily_tasks.remove(task)
        day.save() # Django doesn’t hit the database until you explicitly call save().
        return redirect('/')             # Finally, redirect to the homepage.
