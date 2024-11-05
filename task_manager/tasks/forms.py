from django import forms
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


class TaskForm(forms.ModelForm[Task]):
    name = forms.CharField(label=_("Name"))
    description = forms.CharField(
        label=_("Description"), widget=forms.Textarea(), required=False
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), label=_("Status")
    )
    executor = forms.ModelChoiceField(
        queryset=ServiceUser.objects.all(), label=_("Executor")
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(), label=_("Labels"), required=False
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
