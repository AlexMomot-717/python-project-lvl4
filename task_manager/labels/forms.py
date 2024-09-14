from django import forms
from task_manager.labels.models import Label


class LabelForm(forms.ModelForm[Label]):
    class Meta:
        model = Label
        fields = ("name",)
