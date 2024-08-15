from django import forms
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm[Task]):

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor")
