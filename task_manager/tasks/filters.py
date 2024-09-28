from django import forms
from django.utils.translation import gettext as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


class TaskFilter(FilterSet):
    def list_request_user_tasks(self, queryset, args, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    status = ModelChoiceFilter(queryset=Status.objects.all(), label=_("Status"))
    executor = ModelChoiceFilter(
        queryset=ServiceUser.objects.all(), label=_("Executor")
    )
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_("Label"))
    request_user_tasks = BooleanFilter(
        method="list_request_user_tasks",
        widget=forms.CheckboxInput,
        label=_("My tasks only"),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]
