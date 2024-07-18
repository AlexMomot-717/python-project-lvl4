from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import ServiceUser


class ServiceUserForm(UserCreationForm[ServiceUser]):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = ServiceUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )
