from django.http import HttpRequest
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label=_("Status"))
    executor = ModelChoiceFilter(queryset=ServiceUser.objects.all(), label=_("Executor"))
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_("Label"))
    # author = ModelChoiceFilter(queryset=ServiceUser.objects.all(), label=_("Self tasks only"))
    # author = BooleanFilter(field_name="author", label=_("Self tasks only"))
    # author = ModelChoiceFilter(queryset=ServiceUser.objects.get(id=request.user.id), label=_("Self tasks only"))

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "author"]
        
    
    # @property
    # def qs(self):
    #     parent = super().qs
    #     author = getattr(self.request, "user")
    # 
    #     return parent.filter(author=author)
