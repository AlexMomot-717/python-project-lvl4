from django import forms
from django.utils.translation import gettext as _

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm[Task]):   
    name = forms.CharField(label=_("Name"))
    description = forms.CharField(label=_("Description"))
    status = forms.ChoiceField(label=_("Status"))
    executor = forms.ChoiceField(label=_("Executor"))
    labels = forms.ChoiceField(label=_("Labels"))

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
