from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.views import generic
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .models import *
from .forms import *
from .serializers import *
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def home(request):
    tasks = Task.objects.filter(task_user=request.user)
    days = Day.objects.all()
    today = Day.objects.get_or_create(date=datetime.date.today())[0] 
    goals = Goal.objects.all().order_by("priority")
    return render(request, "home_tasks.html", {"tasks":tasks, "days":days, "goals":goals, "today":today})

def add_task(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save_user(request)
        else:
            print("form not valid")
            print(form.errors)
            print(request.POST.get('task_goal'))
    return redirect('/')             # Finally, redirect to the homepage.

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

def history(request):
    tasks = Task.objects.all()
    days = Day.objects.all()
    return render(request, "history.html", {"tasks":tasks, "days":days})

class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    **Multiple inheritance**
    The generic view will query the database to get all records for 
    the specified model (Task) then render a template located at 
    templates/{tasks_app}/{task}_list.html
    """
    model = Task
    #queryset = Task.objects.filter(task_user=self.request.user)# Get tasks for that user
    def get_queryset(self):
        return Task.objects.filter(task_user=self.request.user)