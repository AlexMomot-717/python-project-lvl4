from django import forms
from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm[Status]):

    class Meta:
        model = Status
        fields = ("name",)
