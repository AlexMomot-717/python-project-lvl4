from django import forms
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm[Status]):
    name = forms.CharField(label=_("Name"))

    class Meta:
        model = Status
        fields = ("name",)
