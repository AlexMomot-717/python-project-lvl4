from django.utils.translation import gettext as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label=_("Status"))
    executor = ModelChoiceFilter(
        queryset=ServiceUser.objects.all(), label=_("Executor")
    )
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_("Label"))
    author = BooleanFilter(field_name="author", label=_("Self tasks only"))

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "author"]

    @property
    def qs(self):
        parent = super().qs

        if request := self.request:
            author = getattr(request, "user", None)
            if author and request.GET.get("author", "") == "true":
                return parent.filter(author=author)

        return parent
