from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:task_id>/remove_task/', views.remove_task, name='remove_task'),
    path('<int:goal_id>/remove_goal/', views.remove_goal, name='remove_goal'),
    path('<int:task_id>/add_task_to_daily_tasks/', views.add_task_to_daily_tasks, name='add_task_to_daily_tasks'),
    path('<int:task_id>/remove_task_from_daily_tasks/', views.remove_task_from_daily_tasks, name='remove_task_from_daily_tasks'),
    path('add_goal/', views.add_goal, name='add_goal'),
    path('<int:task_id>/task_done/', views.task_done, name='task_done'),
]