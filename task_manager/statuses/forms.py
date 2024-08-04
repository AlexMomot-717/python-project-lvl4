from django import forms
from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm[Status]):
    name = forms.CharField()

    class Meta:
        model = Status
        fields = ("name",)
