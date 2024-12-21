from typing import Any

from django import forms
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
        label_suffix="",
    )
    executor = ModelChoiceFilter(
        queryset=ServiceUser.objects.all(),
        label=_("Executor"),
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
        label_suffix="",
    )
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        widget=forms.Select(attrs={"class": "form-select ml-2 mr-3"}),
        label_suffix="",
    )
    request_user_tasks = BooleanFilter(
        method="list_request_user_tasks",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mr-3"}),
        label=_("My tasks only"),
        label_suffix="",
    )

    def list_request_user_tasks(
        self, queryset: QuerySet[Task], args: dict[str, Any], value: bool
    ) -> QuerySet[Task]:
        if value:
            self.form.fields["request_user_tasks"].widget.attrs.update(
                {"class": "form-check-input mr-3 is-valid"}
            )
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]
