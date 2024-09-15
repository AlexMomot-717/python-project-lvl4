from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from task_manager.users.models import ServiceUser


class ServiceUserForm(UserCreationForm[ServiceUser]):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

    class Meta:
        model = ServiceUser
        fields = ("first_name", "last_name", "username", "password1", "password2")
