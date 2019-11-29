from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
    def save_user(self, request):
        obj = self.save(commit=False)
        obj.task_user = request.user
        obj.save()
        self.save()
        
        

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'

