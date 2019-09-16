from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'

