from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import ServiceUser


class ServiceUserForm(UserCreationForm[ServiceUser]):

    class Meta:
        model = ServiceUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )  # noqa: E501
